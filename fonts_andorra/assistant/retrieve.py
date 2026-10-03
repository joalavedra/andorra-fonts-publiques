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


def _govern_chunk_score(heading: str, chunk: str, query_terms: set[str]) -> int:
    heading_terms = set(index.tokenize(heading))
    chunk_terms = set(index.tokenize(chunk))
    normalized = normalize(chunk)
    has_amount = bool(re.search(r"€|\beuros?\b|%", normalized, re.IGNORECASE))
    has_duration = bool(re.search(
        r"\b\d+(?:[.,]\d+)?\s*(?:anys?|dies?|mesos?|hores?|years?|days?|months?)\b",
        normalized,
        re.IGNORECASE,
    ))
    return len(query_terms & chunk_terms) + 2 * len(query_terms & heading_terms) + 3 * int(
        has_amount or has_duration
    )


def _govern_chunks(text: str, max_chars: int = 400) -> list[str]:
    sentences = re.split(r"(?<=[.;:])\s+", text.strip())
    segments = []
    for sentence in sentences:
        if len(sentence) <= max_chars:
            segments.append(sentence)
            continue
        words = sentence.split()
        segment = ""
        for word in words:
            pieces = [word[index:index + max_chars] for index in range(0, len(word), max_chars)]
            for piece in pieces:
                candidate = f"{segment} {piece}".strip()
                if segment and len(candidate) > max_chars:
                    segments.append(segment)
                    segment = piece
                else:
                    segment = candidate
        if segment:
            segments.append(segment)

    chunks = []
    current = ""
    for segment in segments:
        candidate = f"{current} {segment}".strip()
        if current and len(candidate) > max_chars:
            chunks.append(current)
            current = segment
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


def _govern_passage(detail: dict, query: str, max_chars: int = 4000) -> str:
    lines = [f"Title: {detail.get('title') or 'Govern d’Andorra page'}"]
    description = detail.get("description", "")
    if description:
        lines.append(f"Description: {description[:1500]}")
    header = "\n".join(lines)
    if len(header) >= max_chars:
        return header[:max_chars]
    query_terms = set(index.tokenize(query))
    chunks = []
    for section_order, (heading, text) in enumerate(detail.get("sections", {}).items()):
        for chunk_order, chunk in enumerate(_govern_chunks(text)):
            chunks.append((
                -_govern_chunk_score(heading, chunk, query_terms),
                section_order,
                chunk_order,
                heading,
                chunk,
            ))
    chunks.sort(key=lambda item: item[:3])

    selected: dict[int, tuple[str, list[tuple[int, str]]]] = {}
    used = len(header)
    for _, section_order, chunk_order, heading, chunk in chunks:
        current = selected.get(section_order)
        cost = len(" … ") + len(chunk) if current else len(heading) + 3 + len(chunk) + 1
        if used + cost > max_chars:
            continue
        if current:
            current[1].append((chunk_order, chunk))
        else:
            selected[section_order] = (heading, [(chunk_order, chunk)])
        used += cost

    passage_lines = [header]
    for section_order in sorted(selected):
        heading, section_chunks = selected[section_order]
        section_chunks.sort(key=lambda item: item[0])
        passage_lines.append(f"{heading}: " + " … ".join(chunk for _, chunk in section_chunks))
    return "\n".join(passage_lines)


def _rank_candidates(
    items: list[dict],
    keywords: list[str],
    index_ranks: dict[str, tuple[int, ...]] | None = None,
) -> list[dict]:
    terms = set()
    for keyword in llm.clean_keywords(keywords):
        terms.update(_tokens(keyword))
    index_ranks = index_ranks or {}
    ranked = []
    for item_order, item in enumerate(items):
        code = item.get("code", "")
        candidate = _tokens(f"{item.get('title', '')} {item.get('url', '')}")
        overlap = sum(
            any(_token_matches(term, candidate_term) for candidate_term in candidate)
            for term in terms
        )
        if code in index_ranks:
            priority = (0, *index_ranks[code])
        else:
            priority = (1, item_order)
        ranked.append((-overlap, *priority, code, item))
    ranked.sort(key=lambda entry: entry[:-1])
    return [entry[-1] for entry in ranked]


def retrieve(question: str) -> list[Source]:
    safe_question, _ = redact(question)
    try:
        keywords = llm.keywords(safe_question)
    except (requests.RequestException, RuntimeError, ValueError):
        keywords = []
    keywords = llm.clean_keywords(keywords)
    candidates: dict[str, dict] = {}
    index_ranks: dict[str, tuple[int, ...]] = {}
    index_order = 0
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
                rank = (result_rank, index_order)
                if code not in index_ranks or rank < index_ranks[code]:
                    index_ranks[code] = rank
                index_order += 1
        except (RuntimeError, ValueError) as exc:
            logger.debug("Procedure index search failed: %s", exc)
    scored = _rank_candidates(list(candidates.values()), keywords, index_ranks)
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
    govern_query = " ".join(keywords) if keywords else safe_question
    try:
        govern_items = index.search(govern_query, limit=3, source="govern.ad")
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
