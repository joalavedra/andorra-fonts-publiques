"""Compact stdio MCP server for the Andorra source catalog and live clients."""

# ruff: noqa: BLE001

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from fonts_andorra import catalog, index
from fonts_andorra.clients import arcgis, bopa, estadistica, feeds, govern, tramits

server = FastMCP("andorra-fonts-publiques")


def _json(value) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)


def _safe(callable_, *args, **kwargs) -> str:
    try:
        return _json(callable_(*args, **kwargs))
    except Exception as exc:
        return _json({"error": str(exc)})


@server.tool()
def search_catalog(query: str, limit: int = 5) -> str:
    """Search the Andorra source catalog."""
    try:
        matches = catalog.search(query, max(0, min(limit, 20)))
        return _json([{
            "id": item["id"],
            "name": item["name"],
            "summary": item["summary"],
            "base_url": item["base_url"],
            "status": item["status"],
        } for item in matches])
    except Exception as exc:
        return _json({"error": str(exc)})


@server.tool()
def source(id: str) -> str:
    """Return one source fiche by id."""
    try:
        item = catalog.source(id)
        return _json(item) if item is not None else _json({"error": f"Unknown source: {id}"})
    except Exception as exc:
        return _json({"error": str(exc)})


@server.tool()
def bopa_search(text: str, date_from: str | None = None, date_to: str | None = None, limit: int = 10) -> str:
    """Search official bulletin documents."""
    return _safe(bopa.search, text, date_from, date_to, size=max(0, min(limit, 50)))


@server.tool()
def bopa_document(name: str, max_chars: int = 20000, offset: int = 0) -> str:
    """Fetch and excerpt a BOPA document by name."""
    try:
        results = bopa.search(name, size=5)
        meta = next((item for item in results["items"] if item["name"] == name), None)
        if meta is None and results["items"]:
            meta = results["items"][0]
        if meta is None:
            return _json({"error": f"No BOPA document matched {name!r}"})
        text = bopa.document_text(meta)
        offset = max(0, offset)
        max_chars = max(0, min(max_chars, 50000))
        return _json({"document": meta, "offset": offset, "text": text[offset:offset + max_chars],
                      "truncated": offset + max_chars < len(text)})
    except Exception as exc:
        return _json({"error": str(exc)})


@server.tool()
def stats_search(text: str, language: str = "ca") -> str:
    """Search Andorra statistical tables."""
    try:
        items = estadistica.search(text, language)
        return _json({"items": items[:50], "total": len(items), "truncated": len(items) > 50})
    except Exception as exc:
        return _json({"error": str(exc)})


@server.tool()
def stats_data(id_division: int, start: str | None = None, end: str | None = None,
               language: str = "ca", max_rows: int = 200) -> str:
    """Read rows from a JSON-stat table."""
    try:
        rows = estadistica.data(id_division, start, end, language)
        max_rows = max(0, min(max_rows, 1000))
        return _json({"rows": rows[:max_rows], "total": len(rows), "truncated": len(rows) > max_rows})
    except Exception as exc:
        return _json({"error": str(exc)})


@server.tool()
def tramits_search(text: str, limit: int = 10) -> str:
    """Search e-tramits procedures."""
    return _search_tramits(text, limit)


def _search_tramits(text: str, limit: int) -> str:
    try:
        return _json({"items": tramits.search(text)[:max(0, min(limit, 50))]})
    except Exception as exc:
        return _json({"error": str(exc)})


@server.tool()
def tramit(code: str, lang: str = "ca") -> str:
    """Read one e-tramits procedure page."""
    try:
        detail = tramits.procedure(code, lang)
        sections = {}
        remaining = 12000
        for heading, text in detail["sections"].items():
            if remaining <= 0:
                break
            excerpt = text[:min(4000, remaining)]
            sections[heading] = excerpt
            remaining -= len(excerpt)
        detail["sections"] = sections
        detail["documents"] = detail["documents"][:20]
        return _json(detail)
    except Exception as exc:
        return _json({"error": str(exc)})


@server.tool()
def govern_search(text: str, limit: int = 10) -> str:
    """Search Govern pages in the committed local index."""
    try:
        items = index.search(text, max(0, min(limit, 50)), source="govern.ad")
        return _json({"items": items})
    except Exception as exc:
        return _json({"error": str(exc)})


@server.tool()
def govern_page(url: str, max_chars: int = 12000) -> str:
    """Fetch one live Govern page and excerpt its sections."""
    try:
        detail = govern.page(url)
        sections = {}
        remaining = max(0, min(max_chars, 50000))
        for heading, text in detail["sections"].items():
            if remaining <= 0:
                break
            excerpt = text[:min(4000, remaining)]
            sections[heading] = excerpt
            remaining -= len(excerpt)
        detail["sections"] = sections
        return _json(detail)
    except Exception as exc:
        return _json({"error": str(exc)})


@server.tool()
def geo_query(layer: str, where: str = "1=1", limit: int = 50) -> str:
    """Query a layer in the curated ArcGIS whitelist."""
    try:
        url = arcgis.resolve(layer)
        rows = arcgis.query(url, where=where, limit=max(0, min(limit, 50)))
        return _json({"layer": layer, "items": rows})
    except Exception as exc:
        return _json({"error": str(exc)})


@server.tool()
def feed_latest(feed: str, limit: int = 10) -> str:
    """Return recent items from official parliamentary or AFA feeds."""
    try:
        items = feeds.latest(feed, max(0, min(limit, 20)))
        for item in items:
            if item.get("title"):
                item["title"] = item["title"][:300]
            if item.get("summary"):
                item["summary"] = item["summary"][:2000]
        return _json(items)
    except Exception as exc:
        return _json({"error": str(exc)})


def main() -> None:
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
