"""Client for Govern d'Andorra information pages and their Catalan sitemap."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlparse

from fonts_andorra.clients import http

BASE = "https://www.govern.ad"
LANGUAGES = {"ca", "es", "fr", "en"}
TITLE_SUFFIX_RE = re.compile(r"\s*-\s*Govern d[’']Andorra\s*$", re.IGNORECASE)


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def _valid_govern_url(url: str) -> bool:
    parsed = urlparse(url)
    return (
        parsed.scheme == "https"
        and parsed.hostname == "www.govern.ad"
        and parsed.port in {None, 443}
        and parsed.username is None
        and parsed.password is None
    )


def _sitemap_url(lang: str) -> str:
    if lang not in LANGUAGES:
        raise ValueError("lang must be ca, es, fr or en")
    return f"{BASE}/{lang}/sitemap.xml"


def sitemap(lang: str = "ca", include_news: bool = False) -> list[dict]:
    """Return sitemap URLs and last-modified values for one language."""
    response = http.get(_sitemap_url(lang))
    response.raise_for_status()
    try:
        root = ET.fromstring(response.content)
    except ET.ParseError:
        xml = response.content.decode("utf-8-sig")
        xml, repairs = re.subn(r"<url>\s*(?=<url>)", "", xml)
        if not repairs:
            raise
        root = ET.fromstring(xml)
    items = []
    for entry in root.iter():
        if _local_name(entry.tag) != "url":
            continue
        values = {_local_name(child.tag): (child.text or "").strip() for child in entry}
        url = values.get("loc", "")
        if not url or (not include_news and "/w/" in urlparse(url).path):
            continue
        items.append({"url": url, "lastmod": values.get("lastmod") or None})
    return items


class _Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.div_depth = 0
        self.articles: list[dict] = []
        self.sections: dict[str, str] = {}
        self.skip_tags: list[str] = []
        self.in_title = False
        self.title_parts: list[str] = []
        self.title = ""
        self.og_title = ""
        self.description = ""
        self.lang = ""

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if tag == "html":
            self.lang = attr.get("lang", "")
        elif tag == "title":
            self.in_title = True
            self.title_parts = []
        elif tag == "meta":
            if attr.get("property", "").lower() == "og:title":
                self.og_title = attr.get("content", "")
            elif attr.get("name", "").lower() == "description":
                self.description = attr.get("content", "")
        if tag in {"script", "style"}:
            self.skip_tags.append(tag)
        if tag == "div":
            self.div_depth += 1
            classes = (attr.get("class") or "").split()
            if "journal-content-article" in classes:
                heading = (attr.get("data-analytics-asset-title") or "").strip()
                discarded = (
                    not heading
                    or heading in {"Prefooter", "Redes sociales"}
                    or heading.endswith("-Tabs")
                )
                self.articles.append({
                    "depth": self.div_depth,
                    "heading": heading,
                    "parts": None if discarded else [],
                })

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
            self.title = " ".join(" ".join(self.title_parts).split())
        if tag in {"script", "style"} and self.skip_tags:
            for index in range(len(self.skip_tags) - 1, -1, -1):
                if self.skip_tags[index] == tag:
                    del self.skip_tags[index]
                    break
        if tag == "div":
            if self.articles and self.articles[-1]["depth"] == self.div_depth:
                article = self.articles.pop()
                parts = article["parts"]
                text = " ".join(" ".join(parts).split()) if parts is not None else ""
                if text:
                    heading = article["heading"]
                    previous = self.sections.get(heading, "")
                    self.sections[heading] = " ".join(value for value in (previous, text) if value)
            self.div_depth = max(0, self.div_depth - 1)

    def handle_data(self, data):
        if self.skip_tags:
            return
        if self.in_title:
            self.title_parts.append(data)
        if self.articles and self.articles[-1]["parts"] is not None:
            self.articles[-1]["parts"].append(data)


def page(url: str) -> dict:
    """Fetch one Govern page and extract its titled content sections."""
    if not _valid_govern_url(url):
        raise ValueError("url must use https://www.govern.ad")
    response = http.get(url)
    response.raise_for_status()
    final_url = response.url
    if not _valid_govern_url(final_url):
        raise ValueError("Govern page redirected outside https://www.govern.ad")
    parser = _Page()
    parser.feed(response.text)
    title = parser.title or parser.og_title
    title = TITLE_SUFFIX_RE.sub("", title).strip()
    lang = parser.lang.split("-", 1)[0].lower() or urlparse(final_url).path.strip("/").split("/", 1)[0]
    return {
        "url": final_url,
        "title": title,
        "description": " ".join(parser.description.split()),
        "lang": lang,
        "sections": parser.sections,
    }
