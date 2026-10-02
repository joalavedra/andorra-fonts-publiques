"""Client for BOPA's frontend-discovered Azure Functions API and document blobs."""

from __future__ import annotations

import html
import re
from html.parser import HTMLParser
from threading import Lock
from urllib.parse import urljoin

import requests

from fonts_andorra.clients import http

HOME = "https://www.bopa.ad/"
API = "https://bopaazurefunctions.azurewebsites.net/api"
BLOB = "https://bopadocuments.blob.core.windows.net/bopa-documents"
ORDER_BY = "AnyButlleti desc, NumButlleti desc, DataArticle desc,OrganismeOrder,OrganismeChildOrder"
_FUNCTION_KEYS: dict[str, str] | None = None
_KEY_LOCK = Lock()


class _Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style"} and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip and data.strip():
            self.parts.append(data.strip())


def normalize_search(text: str) -> str:
    replacements = str.maketrans({"à": "a", "á": "a", "è": "e", "é": "e", "í": "i", "ì": "i",
                                  "ò": "o", "ó": "o", "ù": "u", "ú": "u", "%": "percentage"})
    return text.lower().translate(replacements)


def _function_keys(refresh: bool = False) -> dict[str, str]:
    global _FUNCTION_KEYS
    with _KEY_LOCK:
        if _FUNCTION_KEYS is not None and not refresh:
            return _FUNCTION_KEYS
        response = http.get(HOME)
        response.raise_for_status()
        bundles = re.findall(r"""(?:src=["'])([^"']*?/static/js/main\.[^"']+\.js)["']""", response.text)
        if not bundles:
            bundles = re.findall(r"""(["'])(/static/js/main\.[^"']+\.js)\1""", response.text)
            bundles = [match[1] for match in bundles]
        discovered: dict[str, str] = {}
        for bundle in bundles:
            js = http.get(urljoin(HOME, bundle))
            js.raise_for_status()
            discovered.update(dict(re.findall(r"/api/(\w+)\?code=([^\"']+)", js.text)))
        if not discovered:
            raise RuntimeError("BOPA frontend bundle contained no API function keys")
        _FUNCTION_KEYS = discovered
        return discovered


def _call(function: str, method: str, *, refresh: bool = False, **kwargs):
    keys = _function_keys(refresh=refresh)
    if function not in keys:
        raise RuntimeError(f"BOPA function {function!r} was not found in the frontend bundle")
    request_kwargs = dict(kwargs)
    extra_params = request_kwargs.pop("params", {})
    params = {"code": keys[function], **extra_params}
    try:
        response = http.request(method, f"{API}/{function}", params=params, **request_kwargs)
    except requests.RequestException:
        raise RuntimeError(f"BOPA request to {function} failed") from None
    if response.status_code in (401, 403) and not refresh:
        return _call(function, method, refresh=True, params=extra_params, **request_kwargs)
    try:
        response.raise_for_status()
    except requests.HTTPError:
        raise RuntimeError(f"BOPA request to {function} returned HTTP {response.status_code}") from None
    if not response.content:
        return {}
    return response.json()


def _items(payload) -> list[dict]:
    if isinstance(payload, list):
        return payload
    for key in ("results", "documents", "items", "value", "Documents", "paginatedDocuments"):
        candidate = payload.get(key) if isinstance(payload, dict) else None
        if isinstance(candidate, list):
            return [
                item["document"] if isinstance(item, dict) and isinstance(item.get("document"), dict) else item
                for item in candidate
                if isinstance(item, dict)
            ]
    return []


def _date(value) -> str | None:
    if not value:
        return None
    return str(value)[:10]


def document_url(nomDocument: str, pub_date: str, num: int | str, fmt: str) -> str:
    publication_year = int(str(pub_date)[:4])
    folder = f"{publication_year - 1988:03d}{int(num):03d}"
    extension = fmt.lower().lstrip(".")
    if extension not in {"html", "pdf"}:
        raise ValueError("fmt must be html or pdf")
    return f"{BLOB}/{folder}/{extension}/{nomDocument}.{extension}"


def normalize_document(item: dict) -> dict:
    name = item.get("nomDocument") or item.get("metadata_storage_name") or ""
    pub_date = _date(item.get("dataPublicacioButlleti") or item.get("dataPublicacio") or item.get("pub_date"))
    bulletin = item.get("numButlleti") or item.get("numBOPA") or item.get("bulletin")
    year = item.get("anyButlleti") or (int(pub_date[:4]) if pub_date else None)
    raw_path = item.get("metadata_storage_path") or ""
    file_type = str(item.get("fileType") or "").lower()
    html_url = item.get("html_url") or (raw_path if raw_path.endswith(".html") else None)
    pdf_url = item.get("pdf_url") or (raw_path if raw_path.endswith(".pdf") else None)
    if name and pub_date and bulletin is not None:
        if not html_url and "pdf" not in file_type:
            html_url = document_url(name, pub_date, bulletin, "html")
        if not pdf_url:
            pdf_url = document_url(name, pub_date, bulletin, "pdf")
    return {
        "name": name,
        "date": pub_date,
        "bulletin": bulletin,
        "year": year,
        "organisme": item.get("organisme"),
        "tema": item.get("tema"),
        "summary": item.get("sumari") or item.get("summary"),
        "html_url": html_url,
        "pdf_url": pdf_url,
    }


def search(text: str = "", date_from: str | None = None, date_to: str | None = None,
           organismes: list | None = None, temes: list | None = None, size: int = 25, skip: int = 0) -> dict:
    date_filter = []
    if date_from:
        date_filter.append({"filterType": "ge", "filterValue": date_from})
    if date_to:
        date_filter.append({"filterType": "le", "filterValue": date_to})
    body = {
        "textSearch": normalize_search(text),
        "temaFilter": temes or [],
        "dateFilter": date_filter,
        "organismeFilter": organismes or [],
        "butlletiFilter": "",
        "anyFilter": [],
        "size": size,
        "skip": skip,
        "orderBy": ORDER_BY,
        "searchMode": 1,
    }
    payload = _call("GetPaginatedDocuments2Indexes", "POST", json=body)
    total = payload.get("totalCount", payload.get("count")) if isinstance(payload, dict) else None
    return {"total": total, "items": [normalize_document(item) for item in _items(payload)]}


def bulletin(year: int, num: int) -> list[dict]:
    if year is None:
        raise ValueError("year is required")
    found: list[dict] = []
    seen: set[str] = set()
    skip, size = 0, 100
    while True:
        payload = _call("GetDocumentsByBOPA", "GET", params={"numBOPA": num, "year": year, "size": size, "skip": skip})
        page = [normalize_document(item) for item in _items(payload)]
        fresh = [item for item in page if item["name"] not in seen]
        found.extend(fresh)
        seen.update(item["name"] for item in fresh)
        if not page or not fresh or len(page) < size:
            break
        skip += len(page)
    return found


def document_text(meta: dict) -> str:
    if not meta.get("html_url"):
        return f"PDF-only document: {meta.get('pdf_url') or ''}".strip()
    response = http.get(meta["html_url"])
    if response.ok:
        parser = _Text()
        parser.feed(response.text)
        text = html.unescape(" ".join(parser.parts))
        if text:
            return text
    return f"PDF-only document: {meta.get('pdf_url') or ''}".strip()
