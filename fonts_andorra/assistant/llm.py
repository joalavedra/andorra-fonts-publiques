"""Gemini plain-REST wrapper; all submitted text is redacted first."""

from __future__ import annotations

import json
import os
import re

from fonts_andorra.assistant.redact import redact
from fonts_andorra.catalog import normalize
from fonts_andorra.clients import http

DEFAULT_MODEL = "gemini-2.5-flash"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
KEYWORD_STOPWORDS = {
    "preu", "cost", "coste", "precio", "prix",
    "termini", "plazo", "deadline", "temps", "tiempo", "time", "duration",
    "quant", "cuanto", "how", "much", "como", "combien", "comment",
    "tramit", "tramits", "procediment", "procediments", "procedimiento", "procedure", "procedures",
    "sollicitud", "sollicituds", "solicitud", "solicitudes", "request", "application",
    "the", "for", "with", "and", "what", "when", "does", "want", "my", "which", "where",
    "un", "una", "del", "amb", "para", "por", "que", "hasta", "cuando",
}


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


def clean_keywords(values: list[str]) -> list[str]:
    result = []
    seen = set()
    for value in values:
        words = re.findall(r"[^\W_]+", str(value).replace("·", ""), re.UNICODE)
        phrase = " ".join(
            word for word in words
            if len(normalize(word)) > 2 and normalize(word) not in KEYWORD_STOPWORDS
        )
        normalized = normalize(phrase)
        if phrase and normalized not in seen:
            result.append(phrase)
            seen.add(normalized)
        if len(result) == 4:
            break
    return result


def keywords(question: str) -> list[str]:
    safe_question, _ = redact(question)
    response = generate(
        "Return a JSON array of 2–4 short Catalan noun phrases naming the same procedure asked about. "
        "Translate the intent faithfully into words likely to appear in an e-tramits title. "
        "Keep the question's distinctive subject and proper names; do not invent another topic or suggest "
        "unrelated procedures. Usually return two variants of that one procedure. "
        "Exclude words about price, cost, time, deadlines, how, or generic procedure/request terms "
        "(preu, cost, termini, temps, quant, tràmit, procediment, sol·licitud). "
        "Examples: first car registration -> [\"matriculació vehicle\", \"primera matriculació\"]; "
        "shop opening hours -> [\"horaris comercials\", \"ampliació horaris\"]; "
        "taxi driver's licence -> [\"carnet de xofer de taxi\", \"llicència de taxi\"]; "
        "duplicate lost immigration card -> [\"duplicat tarja immigració\", \"duplicat targeta immigració\"]; "
        "Pla Engega electric vehicle grant -> [\"ajut Pla Engega\", \"ajut vehicle elèctric\"]. "
        "Output only the JSON array.\nQuestion: " + safe_question,
        system_instruction=(
            "Return only 2–4 concise Catalan title phrases for the procedure the question is actually about. "
            "Preserve its distinguishing topic; never substitute an unrelated procedure. "
            "Do not answer the question. Exclude cost, time, deadline, how, and generic procedure words."
        ),
    )
    match = re.search(r"\[[\s\S]*\]", response)
    if not match:
        raise ValueError("Gemini did not return a JSON keyword array")
    values = json.loads(match.group(0))
    if not isinstance(values, list):
        raise TypeError("Gemini keyword response must be a JSON array")
    return clean_keywords(values)
