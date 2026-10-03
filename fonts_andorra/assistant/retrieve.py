"""Retrieve official procedure, Govern page, and bulletin passages for a question."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass

import requests

from fonts_andorra import index
from fonts_andorra.assistant import llm
from fonts_andorra.assistant.redact import redact
from fonts_andorra.catalog import normalize
from fonts_andorra.clients import bopa, govern, tramits

logger = logging.getLogger(__name__)


@dataclass
class Source:
    n: int
    title: str
    url: str
    text: str


def _tokens(value: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", normalize(value)) if len(token) > 2}


def _token_matches(left: str, right: str) -> bool:
    return left == right or (len(left) >= 5 and len(right) >= 5 and left[:5] == right[:5])


def _section_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", normalize(value)).strip()


def _is_description_heading(heading: str) -> bool:
    name = _section_name(heading)
    return any(name == term or name.startswith(f"{term} ") for term in (
        "descripcio",
        "descripcion",
        "description",
    ))


def _is_key_fact_heading(heading: str) -> bool:
    name = _section_name(heading)
    return (
        name in {"preu", "precio", "prix"}
        or ("resoluc" in name and any(term in name for term in ("maxim", "maximo", "maximum")))
        or (
            any(term in name for term in ("periode", "periodo"))
            and any(term in name for term in ("demanar", "pedir", "demande", "demander"))
        )
    )


def _procedure_passage(detail: dict, fallback_title: str = "", max_chars: int = 2500) -> str:
    facts = [
        ("Title", detail.get("title") or fallback_title),
        ("Price", detail.get("price")),
        ("Maximum resolution time", detail.get("max_resolution")),
        ("Application period", detail.get("application_period")),
        ("Online available", detail.get("online_available")),
        ("Appointment required", detail.get("appointment_required")),
    ]
    header = "\n".join(
        f"{label}: {value}"
        for label, value in facts
        if value is not None and str(value).strip()
    )
    sections = [
        (heading, text)
        for heading, text in detail.get("sections", {}).items()
        if text and not _is_key_fact_heading(heading)
    ]
    descriptions = [item for item in sections if _is_description_heading(item[0])]
    remaining = [item for item in sections if not _is_description_heading(item[0])]
    body = "\n".join(f"{heading}: {text}" for heading, text in [*descriptions, *remaining])
    if not body or len(header) >= max_chars:
        return header
    if not header:
        return body[:max_chars]
    return f"{header}\n{body[:max_chars - len(header) - 1]}"


def _govern_section_score(heading: str, text: str, query_terms: set[str]) -> int:
    heading_terms = set(index.tokenize(heading))
    text_terms = set(index.tokenize(text))
    normalized = normalize(text)
    has_amount = bool(re.search(r"€|\beuros?\b|%", normalized, re.IGNORECASE))
    has_duration = bool(re.search(
        r"\b\d+(?:[.,]\d+)?\s*(?:anys?|dies?|mesos?|hores?|years?|days?|months?)\b",
        normalized,
        re.IGNORECASE,
    ))
    return (
        2 * len(query_terms & heading_terms)
        + len(query_terms & text_terms)
        + 2 * int(has_amount or has_duration)
    )


def _govern_passage(detail: dict, query: str, max_chars: int = 4000) -> str:
    lines = [f"Title: {detail.get('title') or 'Govern d’Andorra page'}"]
    description = detail.get("description", "")
    if description:
        lines.append(f"Description: {description[:1500]}")
    query_terms = set(index.tokenize(query))
    sections = [
        (heading, text, order)
        for order, (heading, text) in enumerate(detail.get("sections", {}).items())
        if text
    ]
    sections.sort(
        key=lambda item: (-_govern_section_score(item[0], item[1], query_terms), item[2])
    )
    passage = "\n".join(lines)
    for heading, text, _ in sections:
        label = f"{heading}: "
        remaining = max_chars - len(passage) - 1
        if remaining <= len(label):
            break
        excerpt = text[:min(1500, remaining - len(label))]
        passage += f"\n{label}{excerpt}"
    return passage[:max_chars]


def _rank_candidates(
    items: list[dict],
    keywords: list[str],
    site_ranks: dict[str, tuple[int, ...]] | None = None,
    fallback_ranks: dict[str, int] | None = None,
) -> list[dict]:
    terms = set()
    for keyword in llm.clean_keywords(keywords):
        terms.update(_tokens(keyword))
    site_ranks = site_ranks or {}
    fallback_ranks = fallback_ranks or {}
    ranked = []
    for item_order, item in enumerate(items):
        code = item.get("code", "")
        candidate = _tokens(f"{item.get('title', '')} {item.get('url', '')}")
        overlap = sum(
            any(_token_matches(term, candidate_term) for candidate_term in candidate)
            for term in terms
        )
        if code in site_ranks:
            priority = (0, *site_ranks[code])
        else:
            priority = (1, fallback_ranks.get(code, item_order), item_order)
        ranked.append((-overlap, *priority, code, item))
    ranked.sort(key=lambda entry: entry[:-1])
    return [entry[-1] for entry in ranked]


def _fallback(keywords: list[str]) -> list[dict]:
    if not llm.clean_keywords(keywords):
        return []
    try:
        items = tramits.list_all()
    except (requests.RequestException, RuntimeError, ValueError):
        return []
    return _rank_candidates(items, keywords)[:8]


def retrieve(question: str) -> list[Source]:
    safe_question, _ = redact(question)
    try:
        keywords = llm.keywords(safe_question)
    except (requests.RequestException, RuntimeError, ValueError):
        keywords = []
    keywords = llm.clean_keywords(keywords)
    candidates: dict[str, dict] = {}
    site_ranks: dict[str, tuple[int, ...]] = {}
    fallback_ranks: dict[str, int] = {}
    site_order = 0
    for keyword in keywords[:4]:
        try:
            results = index.search(keyword, limit=8, source="e-tramits")
            for result_rank, result in enumerate(results):
                item = dict(result)
                code = item.get("id") or item.get("code")
                if not code:
                    continue
                item["code"] = code
                candidates.setdefault(code, item)
                rank = (1, result_rank, site_order)
                if code not in site_ranks or rank < site_ranks[code]:
                    site_ranks[code] = rank
                site_order += 1
        except (RuntimeError, ValueError) as exc:
            logger.debug("Procedure index search failed: %s", exc)
        try:
            results = tramits.search(keyword)
            for result_rank, item in enumerate(results):
                code = item.get("code")
                if not code:
                    continue
                candidates.setdefault(code, item)
                rank = (0, result_rank, site_order)
                if code not in site_ranks or rank < site_ranks[code]:
                    site_ranks[code] = rank
                site_order += 1
        except (requests.RequestException, RuntimeError, ValueError) as exc:
            logger.debug("Procedure site search failed: %s", exc)
    fallback_items = _fallback(keywords)
    for rank, item in enumerate(fallback_items):
        code = item.get("code")
        if not code:
            continue
        candidates.setdefault(code, item)
        fallback_ranks.setdefault(code, rank)
    scored = _rank_candidates(list(candidates.values()), keywords, site_ranks, fallback_ranks)
    retrieved: list[Source] = []
    for item in scored[:5]:
        try:
            detail = tramits.procedure(item["url"])
        except (requests.RequestException, RuntimeError, ValueError) as exc:
            logger.debug("Procedure retrieval failed: %s", exc)
            continue
        title = detail.get("title") or item.get("title") or item["code"]
        text = _procedure_passage(detail, title)
        retrieved.append(Source(len(retrieved) + 1, title, detail["url"], text))
    govern_query = " ".join([*keywords, safe_question])
    try:
        govern_items = index.search(govern_query, limit=2, source="govern.ad")
    except (RuntimeError, ValueError) as exc:
        logger.debug("Govern index search failed: %s", exc)
        govern_items = []
    for item in govern_items:
        try:
            detail = govern.page(item["url"])
        except Exception as exc:  # noqa: BLE001
            logger.debug("Govern page retrieval failed: %s", exc)
            continue
        title = detail.get("title") or item.get("title") or "Govern d’Andorra page"
        passage = _govern_passage(detail, govern_query)
        retrieved.append(Source(len(retrieved) + 1, title, detail["url"], passage))
    if re.search(
        r"\b(law|legal|regulation|reglament|regulacion|llei|ley|loi|decret|decreto|normativa)\b",
        normalize(question),
    ):
        try:
            results = bopa.search(question, size=3)
            for item in results["items"][:3]:
                text = bopa.document_text(item)
                retrieved.append(Source(len(retrieved) + 1, item.get("name") or "BOPA document",
                                        item.get("html_url") or item.get("pdf_url") or "", text[:2500]))
        except (requests.RequestException, RuntimeError, ValueError) as exc:
            logger.debug("BOPA retrieval failed: %s", exc)
    if not retrieved:
        retrieved.append(Source(1, "e-tramits procedure search", "https://www.e-tramits.ad/tramits/search/",
                                "No matching procedure passage was retrieved."))
    return retrieved
