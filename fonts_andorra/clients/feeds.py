"""RSS and Atom clients using only the Python standard library."""

from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime

import requests

from fonts_andorra.clients import http

logger = logging.getLogger(__name__)

FEEDS = {
    "consell-general": ["https://www.consellgeneral.ad/RSS"],
    "afa": [
        "https://www.afa.ad/RSS",
        "https://www.afa.ad/ca/categories-home/alertes/RSS",
        "https://www.afa.ad/ca/categories-home/comunicats-premsa/RSS",
        "https://www.afa.ad/ca/categories-home/nova-normativa/RSS",
        "https://www.afa.ad/ca/categories-home/educacio-financera/RSS",
    ],
    "afa-alerts": ["https://www.afa.ad/ca/categories-home/alertes/RSS"],
    "afa-press": ["https://www.afa.ad/ca/categories-home/comunicats-premsa/RSS"],
    "afa-regulation": ["https://www.afa.ad/ca/categories-home/nova-normativa/RSS"],
    "afa-financial-education": ["https://www.afa.ad/ca/categories-home/educacio-financera/RSS"],
}


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def _timestamp(value: str | None) -> float:
    if not value:
        return 0
    try:
        return parsedate_to_datetime(value).timestamp()
    except (TypeError, ValueError, OverflowError):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
        except (ValueError, OverflowError):
            return 0


def latest(feed_key: str, limit: int = 10) -> list[dict]:
    if feed_key not in FEEDS:
        raise KeyError(f"Unknown feed: {feed_key}")
    collected = []
    successful_feeds = 0
    failures = []
    for feed_url in FEEDS[feed_key]:
        try:
            response = http.get(
                feed_url,
                headers={"Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml"},
            )
            response.raise_for_status()
            root = ET.fromstring(response.content)
        except (requests.RequestException, ET.ParseError) as exc:
            logger.warning("Skipping unavailable feed %s: %s", feed_url, exc)
            failures.append(exc)
            continue
        successful_feeds += 1
        for item in root.iter():
            if _local_name(item.tag) not in {"item", "entry"}:
                continue
            fields = {}
            for child in list(item):
                name = _local_name(child.tag)
                if name == "link":
                    value = child.attrib.get("href") or (child.text or "").strip()
                else:
                    value = " ".join("".join(child.itertext()).split())
                if value and name not in fields:
                    fields[name] = value
            collected.append({
                "title": fields.get("title"),
                "url": fields.get("link"),
                "date": fields.get("pubdate") or fields.get("published") or fields.get("updated") or fields.get("date"),
                "summary": fields.get("description") or fields.get("summary") or fields.get("content"),
                "feed": feed_key,
            })
    if not successful_feeds and failures:
        raise RuntimeError(f"All {len(FEEDS[feed_key])} feed endpoints failed for {feed_key}") from failures[0]
    unique = {}
    for item in collected:
        unique.setdefault(item["url"] or item["title"], item)
    return sorted(unique.values(), key=lambda item: _timestamp(item["date"]), reverse=True)[:max(0, limit)]
