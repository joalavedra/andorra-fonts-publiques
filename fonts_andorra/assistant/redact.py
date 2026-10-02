"""Mask common direct identifiers before user or source text reaches an LLM."""

from __future__ import annotations

import re

PATTERNS = [
    ("EMAIL", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)),
    (
        "IBAN",
        re.compile(
            r"\b[A-Z]{2}\d{2}(?:[A-Z0-9]{11,30}| ?(?:[A-Z0-9]{4} ){2,7}[A-Z0-9]{1,4})\b",
            re.IGNORECASE,
        ),
    ),
    ("NRT", re.compile(r"\b[A-Z]\d{6}[A-Z]\b", re.IGNORECASE)),
    ("PHONE", re.compile(r"(?<![\w])(?:\+\d{1,3}[\s().-]?)?(?:\d[\s().-]?){6,11}\d(?!\w)")),
    ("PASSPORT", re.compile(r"\b(?:[A-Z]{2}\d{7,9}|[A-Z]\d{7,9})\b", re.IGNORECASE)),
]
DATE_LIKE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def redact(text: str) -> tuple[str, int]:
    count = 0
    result = text
    for label, pattern in PATTERNS:
        def replace(match, label=label):
            nonlocal count
            if label == "PHONE" and DATE_LIKE.fullmatch(match.group(0)):
                return match.group(0)
            count += 1
            return f"[REDACTED_{label}]"

        result = pattern.sub(replace, result)
    return result, count
