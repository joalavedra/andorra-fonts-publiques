"""HTML client for e-tramits search and procedure pages."""

from __future__ import annotations

import json
import re
import time
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse

from fonts_andorra.catalog import normalize
from fonts_andorra.clients import http

BASE = "https://www.e-tramits.ad/tramits"
SEARCH_URL = f"{BASE}/search/"
CACHE_PATH = Path.home() / ".cache" / "fonts-andorra" / "tramits.json"
CODE_RE = re.compile(r"/p/([^/?#]+)", re.IGNORECASE)
TOTAL_RE = re.compile(r"([\d.,]+)\s+resultats?", re.IGNORECASE)
LOGIN_CTA_RE = re.compile(
    r"\s*Cal iniciar sessió per fer el tràmit\s+Sol·licitar-ho ara\s*$",
    re.IGNORECASE,
)
ACCESS_CTA_RE = re.compile(
    r"\s*(?:"
    r"Podeu accedir al tràmit des del següent enllaç"
    r"|Puede acceder al trámite (?:desde|a través de) (?:el siguiente enlace|este enlace)"
    r"|Vous pouvez accéder à (?:la démarche|la procédure) "
    r"(?:depuis|à partir de|via) (?:le lien suivant|ce lien)"
    r"|You can access the procedure (?:from|via) (?:the following link|this link)"
    r")\s*[.!?…,:;]*\s*$",
    re.IGNORECASE,
)


def _text(value: str) -> str:
    return " ".join(value.split())


def _clean_access_cta(value: str) -> str:
    return _text(ACCESS_CTA_RE.sub("", value))


def _section_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", normalize(value)).strip()


def _is_application_period_heading(heading: str) -> bool:
    name = _section_name(heading)
    return (
        ("periode de l any" in name and "demanar" in name)
        or ("periodo del ano" in name and "pedir" in name)
        or ("periode de l annee" in name and ("demande" in name or "demander" in name))
    )


class _Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.anchors: list[dict] = []
        self.links: list[dict] = []
        self.sections: dict[str, list[str]] = {}
        self.heading: str | None = None
        self.headings: list[str] = []
        self.anchor: dict | None = None
        self.heading_parts: list[str] = []
        self.jsonld: list[str] = []
        self.in_jsonld = False
        self.jsonld_parts: list[str] = []
        self.total_text: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if tag in {"script", "style"}:
            self.skip += 1
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.heading = ""
            self.heading_parts = []
        if tag == "a":
            self.anchor = {"href": attr.get("href"), "text": ""}
        if tag == "link" and (attr.get("hreflang") or attr.get("rel") == "alternate"):
            self.links.append({"lang": attr.get("hreflang"), "href": attr.get("href")})
        if tag == "script" and attr.get("type") == "application/ld+json":
            self.in_jsonld = True
            self.jsonld_parts = []

    def handle_endtag(self, tag):
        if tag == "a" and self.anchor is not None:
            self.anchors.append(self.anchor)
            self.anchor = None
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"} and self.heading is not None:
            heading = _text(" ".join(self.heading_parts))
            if heading:
                self.heading = heading
                self.headings.append(heading)
                self.sections.setdefault(heading, [])
        if tag == "script" and self.in_jsonld:
            self.jsonld.append("".join(self.jsonld_parts))
            self.in_jsonld = False
        if tag in {"script", "style"} and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if self.in_jsonld:
            self.jsonld_parts.append(data)
        if self.skip:
            return
        value = _text(data)
        if not value:
            return
        if self.anchor is not None:
            self.anchor["text"] = _text(self.anchor["text"] + " " + value)
        if self.heading is not None and not self.heading:
            self.heading_parts.append(value)
        elif self.heading:
            self.sections.setdefault(self.heading, []).append(value)
        self.total_text.append(value)


def _page(path: str, params: dict | None = None):
    response = http.get(path, params=params)
    response.raise_for_status()
    parser = _Page()
    parser.feed(response.text)
    return response.url, response.text, parser


def _search_page(text: str, page: int, stable_sort: bool = False):
    if stable_sort:
        params = {"q": ":name-asc", "page": page}
    else:
        params = {"text": text}
        if page:
            params["page"] = page
    url, _, parsed = _page(SEARCH_URL, params)
    total_match = TOTAL_RE.search(" ".join(parsed.total_text))
    total = int(total_match.group(1).replace(".", "").replace(",", "")) if total_match else None
    found = []
    for anchor in parsed.anchors:
        href = anchor.get("href") or ""
        match = CODE_RE.search(href)
        if not match:
            continue
        full_url = urljoin(url, href)
        found.append({"code": match.group(1).upper(), "title": anchor["text"], "url": full_url})
    unique = {}
    for item in found:
        unique[item["code"]] = item
    return list(unique.values()), total


def search(text: str = "", page: int = 0) -> list[dict]:
    items, _ = _search_page(text, page)
    return items


def list_all(refresh: bool = False) -> list[dict]:
    if not refresh:
        try:
            cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
            if (isinstance(cache, dict) and isinstance(cache.get("items"), list)
                    and time.time() - cache.get("fetched_at", 0) < 24 * 60 * 60):
                return cache["items"]
        except (OSError, ValueError, TypeError):
            pass
    collected: dict[str, dict] = {}
    total = None
    page = 0
    while total is None or len(collected) < total:
        items, observed_total = _search_page("", page, stable_sort=True)
        if observed_total is not None:
            total = observed_total
        previous = len(collected)
        collected.update((item["code"], item) for item in items)
        if not items or len(collected) == previous:
            break
        page += 1
    result = list(collected.values())
    if total is not None and len(result) < total:
        raise RuntimeError(f"e-tramits stable listing returned {len(result)} of {total} procedures")
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps({"fetched_at": time.time(), "items": result}, ensure_ascii=False), encoding="utf-8")
    return result


def _localized_url(url: str, lang: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != "www.e-tramits.ad":
        raise ValueError("procedure URL must use https://www.e-tramits.ad")
    if lang == "ca":
        return url
    _, _, parser = _page(url)
    alternate = next((link["href"] for link in parser.links
                      if str(link.get("lang", "")).lower().startswith(lang)), None)
    if alternate:
        return urljoin(url, alternate)
    path = parsed.path
    code = CODE_RE.search(path)
    if not code:
        raise ValueError(f"Cannot identify procedure code from {url}")
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query["lang"] = lang
    return urlunparse(parsed._replace(query=urlencode(query)))


def procedure(code_or_url: str, lang: str = "ca") -> dict:
    if lang not in {"ca", "es", "fr"}:
        raise ValueError("lang must be ca, es or fr")
    catalog_title = None
    if code_or_url.startswith(("http://", "https://")):
        url = code_or_url
        code_match = CODE_RE.search(url)
        if not code_match:
            raise ValueError("procedure URL must contain a /p/{code} path")
        code = code_match.group(1).upper()
    else:
        code = code_or_url.upper()
        if not re.fullmatch(r"[A-Z0-9_.-]+", code):
            raise ValueError("procedure code must contain only letters, digits, dots, underscores or hyphens")
        matches = [item for item in search(code) if item["code"] == code]
        if not matches:
            matches = [item for item in list_all() if item["code"] == code]
        if not matches:
            raise LookupError(f"Procedure {code} not found")
        catalog_title = matches[0].get("title")
        url = matches[0]["url"]
    url = _localized_url(url, lang)
    final_url, _, parsed = _page(url)
    sections = {}
    for heading, parts in parsed.sections.items():
        name = _section_name(heading)
        value = _clean_access_cta(" ".join(parts))
        if not value or name in {"canviar representat", "portal de transparencia"}:
            continue
        if name == "temps mitja de presentacio del tramit":
            value = LOGIN_CTA_RE.sub("", value)
        if value:
            sections[heading] = value
    title = next((anchor["text"] for anchor in parsed.anchors if CODE_RE.search(anchor.get("href") or "")
                  and anchor["text"]), "")
    if not title:
        title = next((heading for heading in parsed.headings
                      if heading and _section_name(heading) not in
                      {"canviar representat", "portal de transparencia"}
                      and not heading.lower().startswith("tr.")), "")
    title = title or catalog_title or code
    documents = []
    for anchor in parsed.anchors:
        href = anchor.get("href") or ""
        if href.lower().endswith(".pdf") or "document" in anchor["text"].lower() or "formulari" in anchor["text"].lower():
            documents.append({"title": anchor["text"] or href.rsplit("/", 1)[-1], "url": urljoin(final_url, href)})
    price = next((value for heading, value in sections.items()
                  if _section_name(heading) in {"preu", "precio", "prix"}), None)
    max_resolution = next((value for heading, value in sections.items()
                          if any(term in _section_name(heading) for term in
                                 ("termini de resolucio maxim", "plazo de resolucion maximo",
                                  "delai de resolution maximum", "resolution time title"))), None)
    application_period = next((value for heading, value in sections.items()
                               if _is_application_period_heading(heading)), None)
    if max_resolution:
        duration = re.search(
            r"\b\d+(?:[.,]\d+)?\s*(?:dia/dies|dies|dia|días?|jours?)"
            r"(?:\s+(?:hàbil\(s\)|hàbils|hábiles|ouvrables))?",
            max_resolution,
            re.IGNORECASE,
        )
        if duration:
            max_resolution = duration.group(0)
    full_text = _section_name(" ".join(parsed.total_text))
    online = False if any(term in full_text for term in (
        "el servei no esta disponible en linia",
        "el servicio no esta disponible en linea",
        "le service n est pas disponible en ligne",
    )) else (
        True if any(term in full_text for term in (
            "sol licitar ho ara",
            "cal iniciar sessio per fer el tramit",
            "solicitarlo ahora",
            "demander maintenant",
        )) else None
    )
    appointment = any(term in full_text for term in (
        "demaneu cita previa",
        "cal demanar cita previa",
        "pida cita previa",
        "demandez un rendez vous",
    ))
    for raw in parsed.jsonld:
        try:
            structured = json.loads(raw)
        except ValueError:
            continue
        if isinstance(structured, dict):
            title = title or structured.get("name", "")
            price = price or structured.get("offers", {}).get("price")
    return {
        "code": code,
        "title": title,
        "url": final_url,
        "lang": lang,
        "sections": sections,
        "documents": documents,
        "price": price,
        "max_resolution": max_resolution,
        "application_period": application_period,
        "online_available": online,
        "appointment_required": appointment,
    }
