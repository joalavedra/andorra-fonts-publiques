#!/usr/bin/env python3
"""Build the local title, URL, and section-heading search index from live sources."""

from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fonts_andorra.clients import govern, tramits

INDEX_PATH = ROOT / "fonts_andorra" / "data" / "index.json"


def _fetch_page(item: dict) -> tuple[str, dict | None, bool]:
    try:
        result = govern.page(item["url"])
    except Exception:  # noqa: BLE001
        return item["url"], None, False
    return item["url"], result, result["url"] != item["url"]


def build() -> dict:
    procedures = tramits.list_all(refresh=True)
    if len(procedures) < 600:
        raise RuntimeError(f"e-tramits index contains only {len(procedures)} procedures; expected at least 600")
    items = [
        {
            "source": "e-tramits",
            "id": item["code"],
            "title": item["title"],
            "url": item["url"],
            "headings": [],
        }
        for item in procedures
    ]

    sitemap_items = govern.sitemap(lang="ca", include_news=False)
    kept_by_url: dict[str, dict] = {}
    dropped = 0
    redirected = 0
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(_fetch_page, sitemap_items)
        for original_url, page, was_redirected in results:
            redirected += int(was_redirected)
            if page is None or not page["sections"]:
                dropped += 1
                continue
            final_url = page["url"]
            if final_url in kept_by_url:
                dropped += 1
                continue
            kept_by_url[final_url] = {
                "source": "govern.ad",
                "id": urlparse(final_url).path,
                "title": page["title"],
                "url": final_url,
                "headings": list(page["sections"]),
            }
    if len(kept_by_url) < 800:
        raise RuntimeError(f"govern.ad index contains only {len(kept_by_url)} pages; expected at least 800")
    items.extend(kept_by_url.values())
    items.sort(key=lambda item: (item["source"], item["url"]))
    index = {
        "version": 1,
        "built": datetime.now(timezone.utc).date().isoformat(),
        "items": items,
    }
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"e-tramits kept: {len(procedures)}")
    print(f"govern.ad sitemap non-news: {len(sitemap_items)}")
    print(f"govern.ad kept: {len(kept_by_url)}")
    print(f"govern.ad dropped: {dropped}")
    print(f"govern.ad redirected: {redirected}")
    return index


if __name__ == "__main__":
    build()
