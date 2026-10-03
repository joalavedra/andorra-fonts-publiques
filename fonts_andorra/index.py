"""Deterministic BM25 search over the compact local source index."""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from functools import lru_cache
from importlib.resources import files
from urllib.parse import unquote, urlparse

from fonts_andorra.catalog import normalize

K1 = 1.5
B = 0.75
TOKEN_RE = re.compile(r"[a-z0-9]+")
STOPWORDS = {
    "a", "al", "amb", "and", "are", "as", "at", "but", "by", "com", "como", "con",
    "de", "del", "des", "do", "does", "el", "els", "en", "es", "et", "for", "from",
    "how", "i", "in", "is", "la", "les", "lo", "los", "mais", "mes", "my", "of",
    "on", "or", "per", "por", "pour", "que", "the", "to", "un", "una", "une", "with",
    "y", "aquest", "aquesta", "aquests", "aquestes", "aquel", "aquella", "those", "this",
    "le", "du", "dans", "las", "para", "se", "su", "sur", "avec",
}
SKIPPED_PATH_SEGMENTS = {
    "ca", "tematiques", "ministeris-i-secretaries-d-estat",
}


def tokenize(value: str) -> list[str]:
    """Normalize, filter, and stem words for index matching."""
    tokens = TOKEN_RE.findall(normalize(value))
    return [_stem(token) for token in tokens if len(token) > 2 and token not in STOPWORDS]


def _stem(token: str) -> str:
    if len(token) > 4 and token.endswith("s"):
        token = token[:-1]
    if len(token) > 4 and token[-1] in "aeo":
        token = token[:-1]
    return token[:8]


@lru_cache(maxsize=1)
def _load_index() -> dict:
    path = files("fonts_andorra").joinpath("data").joinpath("index.json")
    return json.loads(path.read_text(encoding="utf-8"))


def _document_tokens(item: dict) -> list[str]:
    title_tokens = tokenize(item.get("title", ""))
    heading_tokens = tokenize(" ".join(item.get("headings", [])))
    path_segments = [
        segment for segment in unquote(urlparse(item.get("url", "")).path).strip("/").split("/")
        if segment and segment not in SKIPPED_PATH_SEGMENTS
    ]
    slug_tokens = tokenize(" ".join(path_segments))
    return title_tokens * 3 + heading_tokens + slug_tokens


def search(query: str, limit: int = 10, source: str | None = None) -> list[dict]:
    """Return deterministic BM25-ranked index entries with positive scores."""
    if limit <= 0:
        return []
    terms = set(tokenize(query))
    if not terms:
        return []
    corpus = [
        item for item in _load_index().get("items", [])
        if source is None or item.get("source") == source
    ]
    if not corpus:
        return []
    document_counters = [Counter(_document_tokens(item)) for item in corpus]
    lengths = [sum(counter.values()) for counter in document_counters]
    average_length = sum(lengths) / len(lengths) or 1
    document_frequency = Counter(
        term for counter in document_counters for term in counter
    )
    scored = []
    for item, counter, length in zip(corpus, document_counters, lengths):
        score = 0.0
        for term in terms:
            frequency = counter.get(term, 0)
            if not frequency:
                continue
            inverse_frequency = math.log(
                1 + (len(corpus) - document_frequency[term] + 0.5)
                / (document_frequency[term] + 0.5)
            )
            normalization = frequency + K1 * (1 - B + B * length / average_length)
            score += inverse_frequency * (frequency * (K1 + 1) / normalization)
        if score > 0:
            result = dict(item)
            result["score"] = round(score, 8)
            scored.append(result)
    scored.sort(key=lambda item: (-item["score"], item["url"]))
    return scored[:limit]
