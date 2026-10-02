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


def _fallback(question: str, keywords: list[str]) -> list[dict]:
    terms = _tokens(" ".join([question, *keywords]))
    try:
        items = tramits.list_all()
    except (requests.RequestException, RuntimeError, ValueError):
        return []
    ranked = []
    for item in items:
        candidate = _tokens(f"{item.get('title', '')} {item.get('url', '')}")
        overlap = len(terms & candidate)
        if overlap:
            ranked.append((-overlap, item["code"], item))
    ranked.sort(key=lambda value: value[:2])
    return [item for _, _, item in ranked[:8]]


def retrieve(question: str) -> list[Source]:
    safe_question, _ = redact(question)
    try:
        keywords = llm.keywords(safe_question)
    except (requests.RequestException, RuntimeError, ValueError):
        keywords = []
    if not keywords:
        words = list(_tokens(safe_question))
        keywords = [" ".join(words[:3])] if words else [safe_question]
        if len(words) > 3:
            keywords.append(" ".join(words[2:5]))
    candidates: dict[str, dict] = {}
    for keyword in keywords[:3]:
        try:
            for item in tramits.search(keyword):
                candidates.setdefault(item["code"], item)
        except (requests.RequestException, RuntimeError, ValueError) as exc:
            logger.debug("Procedure search failed: %s", exc)
            continue
    for item in _fallback(safe_question, keywords):
        candidates.setdefault(item["code"], item)
    scored = []
    query_terms = _tokens(" ".join([safe_question, *keywords]))
    for item in candidates.values():
        overlap = len(query_terms & _tokens(f"{item.get('title', '')} {item.get('url', '')}"))
        scored.append((-overlap, item["code"], item))
    scored.sort(key=lambda value: value[:2])
    retrieved: list[Source] = []
    for _, _, item in scored[:3]:
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
                                detail["url"], text[:4000]))
    if re.search(
        r"\b(law|legal|regulation|reglament|regulacion|llei|ley|loi|decret|decreto|normativa)\b",
        normalize(question),
    ):
        try:
            results = bopa.search(question, size=3)
            for item in results["items"][:3]:
                text = bopa.document_text(item)
                retrieved.append(Source(len(retrieved) + 1, item.get("name") or "BOPA document",
                                        item.get("html_url") or item.get("pdf_url") or "", text[:4000]))
        except (requests.RequestException, RuntimeError, ValueError) as exc:
            logger.debug("BOPA retrieval failed: %s", exc)
    if not retrieved:
        retrieved.append(Source(1, "e-tramits procedure search", "https://www.e-tramits.ad/tramits/search/",
                                "No matching procedure passage was retrieved."))
    return retrieved
