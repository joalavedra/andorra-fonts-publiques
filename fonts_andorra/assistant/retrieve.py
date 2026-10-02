"""Retrieve official procedure and bulletin passages for a question."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass

import requests

from fonts_andorra.assistant import llm
from fonts_andorra.assistant.redact import redact
from fonts_andorra.catalog import normalize
from fonts_andorra.clients import bopa, tramits

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


def _rank_candidates(
    items: list[dict],
    keywords: list[str],
    site_ranks: dict[str, tuple[int, int]] | None = None,
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
    site_ranks: dict[str, tuple[int, int]] = {}
    site_order = 0
    for keyword in keywords[:4]:
        try:
            for result_rank, item in enumerate(tramits.search(keyword)):
                code = item.get("code")
                if not code:
                    continue
                candidates.setdefault(code, item)
                rank = (result_rank, site_order)
                if code not in site_ranks or rank < site_ranks[code]:
                    site_ranks[code] = rank
                site_order += 1
        except (requests.RequestException, RuntimeError, ValueError) as exc:
            logger.debug("Procedure search failed: %s", exc)
            continue
    fallback_items = _fallback(keywords)
    fallback_ranks = {}
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
        text_parts = []
        if detail.get("max_resolution"):
            text_parts.append(f"Maximum resolution time: {detail['max_resolution']}")
        if detail.get("price"):
            text_parts.append(f"Price: {detail['price']}")
        if detail.get("online_available") is not None:
            text_parts.append(f"Online available: {detail['online_available']}")
        if detail.get("appointment_required") is not None:
            text_parts.append(f"Appointment required: {detail['appointment_required']}")
        text_parts.extend(f"{heading}: {value}" for heading, value in detail["sections"].items())
        text = "\n".join(text_parts)
        retrieved.append(Source(len(retrieved) + 1, detail.get("title") or item.get("title") or item["code"],
                                detail["url"], text[:2500]))
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
