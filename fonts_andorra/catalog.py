"""Load the source catalog and perform small accent-insensitive searches."""

from __future__ import annotations

import json
import re
import unicodedata
from importlib.resources import files
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _source_files() -> list[Path]:
    return sorted((ROOT / "sources").glob("*.yaml"))


def load_catalog(path: str | Path | None = None) -> dict:
    if path:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    catalog_path = ROOT / "catalog.json"
    if catalog_path.exists():
        return json.loads(catalog_path.read_text(encoding="utf-8"))
    package_catalog = files("fonts_andorra").joinpath("data").joinpath("catalog.json")
    if package_catalog.is_file():
        return json.loads(package_catalog.read_text(encoding="utf-8"))
    sources = []
    for source_path in _source_files():
        sources.append(yaml.safe_load(source_path.read_text(encoding="utf-8")))
    return {"sources": sources}


def source(source_id: str, catalog: dict | None = None) -> dict | None:
    data = catalog or load_catalog()
    return next((item for item in data.get("sources", []) if item.get("id") == source_id), None)


def normalize(value) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    return "".join(char for char in text if not unicodedata.combining(char)).lower()


def _tokens(value) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", normalize(value)) if len(token) > 1}


def search(query: str, limit: int = 5, catalog: dict | None = None) -> list[dict]:
    data = catalog or load_catalog()
    wanted = _tokens(query)
    ranked = []
    for item in data.get("sources", []):
        searchable = " ".join(str(item.get(key, "")) for key in ("id", "name", "org", "sector", "tags", "summary"))
        tokens = _tokens(searchable)
        overlap = wanted & tokens
        if overlap:
            ranked.append((len(overlap), len(overlap) / max(1, len(wanted)), item))
    ranked.sort(key=lambda entry: (-entry[0], -entry[1], entry[2]["id"]))
    return [entry[2] for entry in ranked[:max(0, limit)]]
