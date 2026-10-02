"""Gemini plain-REST wrapper; all submitted text is redacted first."""

from __future__ import annotations

import json
import os
import re

from fonts_andorra.assistant.redact import redact
from fonts_andorra.clients import http

DEFAULT_MODEL = "gemini-2.5-flash"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def generate(prompt: str, system_instruction: str | None = None) -> str:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is required for the cited assistant")
    model = os.environ.get("FONTS_ANDORRA_MODEL", DEFAULT_MODEL)
    safe_prompt, _ = redact(prompt)
    body = {
        "contents": [{"role": "user", "parts": [{"text": safe_prompt}]}],
        "generationConfig": {"temperature": 0},
    }
    if system_instruction:
        safe_system, _ = redact(system_instruction)
        body["systemInstruction"] = {"parts": [{"text": safe_system}]}
    response = http.post(
        API_URL.format(model=model),
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
        json=body,
    )
    response.raise_for_status()
    payload = response.json()
    return "".join(part.get("text", "") for part in payload["candidates"][0]["content"]["parts"])


def keywords(question: str) -> list[str]:
    safe_question, _ = redact(question)
    response = generate(
        "Return a JSON array of two or three short Catalan search queries for this administrative question. "
        "Output only the JSON array.\nQuestion: " + safe_question,
        system_instruction="Create concise search keywords. Do not answer the question.",
    )
    match = re.search(r"\[[\s\S]*\]", response)
    if not match:
        raise ValueError("Gemini did not return a JSON keyword array")
    values = json.loads(match.group(0))
    return [str(value).strip() for value in values if str(value).strip()][:3]
