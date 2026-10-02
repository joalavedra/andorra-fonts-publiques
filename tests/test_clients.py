import json
from pathlib import Path

import pytest

from fonts_andorra.clients import arcgis, bopa, estadistica, feeds, tramits

FIXTURES = Path(__file__).parent / "fixtures"


def test_bopa_document_url_uses_publication_year():
    url = bopa.document_url("document", "2026-08-28", 100, "html")
    assert url.endswith("/038100/html/document.html")


def test_bopa_search_fixture_normalizes_document():
    payload = json.loads((FIXTURES / "bopa-search.json").read_text(encoding="utf-8"))
    assert bopa._items(payload)
    item = bopa.normalize_document(bopa._items(payload)[0])
    assert set(item) == {"name", "date", "bulletin", "year", "organisme", "tema", "summary", "html_url", "pdf_url"}


def test_bopa_items_unwraps_paginated_documents():
    payload = {"paginatedDocuments": [{"score": 1, "document": {"nomDocument": "example"}}]}
    assert bopa._items(payload) == [{"nomDocument": "example"}]


def test_bopa_refresh_preserves_query_parameters(monkeypatch):
    keys_seen = []
    requests = []

    def function_keys(refresh=False):
        keys_seen.append(refresh)
        return {"GetDocumentsByBOPA": "refreshed" if refresh else "expired"}

    class Response:
        def __init__(self, status_code):
            self.status_code = status_code
            self.content = b""

        def raise_for_status(self):
            return None

    responses = iter((Response(401), Response(200)))
    monkeypatch.setattr(bopa, "_function_keys", function_keys)
    monkeypatch.setattr(
        bopa.http, "request",
        lambda method, url, **kwargs: (requests.append(kwargs) or next(responses)),
    )
    assert bopa._call("GetDocumentsByBOPA", "GET", params={"numBOPA": 100, "year": 2026}) == {}
    assert keys_seen == [False, True]
    assert requests[0]["params"] == {"code": "expired", "numBOPA": 100, "year": 2026}
    assert requests[1]["params"] == {"code": "refreshed", "numBOPA": 100, "year": 2026}


def test_estadistica_fixture_flattens_jsonstat():
    payload = json.loads((FIXTURES / "stats-1070.json").read_text(encoding="utf-8-sig"))
    rows = estadistica.parse_jsonstat(payload)
    assert rows
    assert {"series_code", "series_label", "period", "value"} <= rows[0].keys()
    assert rows[-1]["period"] == "2026-06"
    assert rows[0]["value"] == 3.5


def test_arcgis_converts_esri_milliseconds():
    info = json.loads((FIXTURES / "arcgis-layer.json").read_text(encoding="utf-8"))
    date_field = next(
        (field["name"] for field in info["fields"] if field["type"] == "esriFieldTypeDate"),
        "last_update",
    )
    metadata = info if any(field["name"] == date_field for field in info["fields"]) else {
        "fields": [{"name": date_field, "type": "esriFieldTypeDate"}]
    }
    converted = arcgis._iso_dates({date_field: 0}, metadata)
    assert converted[date_field].startswith("1970-01-01T00:00:00")


def test_arcgis_raises_for_error_json_with_http_200(monkeypatch):
    class Response:
        def raise_for_status(self):
            return None

        def json(self):
            return {"error": {"code": 499, "message": "Token Required", "details": []}}

    monkeypatch.setattr(arcgis.http, "get", lambda *args, **kwargs: Response())
    with pytest.raises(arcgis.ArcgisError, match="499 Token Required"):
        arcgis._json("https://example.invalid/FeatureServer/0")


def test_tramits_search_parser_handles_results(monkeypatch):
    content = (FIXTURES / "tramits-search.html").read_text(encoding="utf-8")
    parsed = tramits._Page()
    parsed.feed(content)
    requested = {}

    def page(path, params=None):
        requested.update(params or {})
        return path, content, parsed

    monkeypatch.setattr(tramits, "_page", page)
    items = tramits.search("vehicle")
    assert items
    assert requested["text"] == "vehicle"
    assert "q" not in requested
    assert [item["code"] for item in items] == ["GV000001", "TR-IEI-FIRST"]
    assert all(item["url"] for item in items)
    requested.clear()
    tramits._search_page("", 7, stable_sort=True)
    assert requested == {"page": 7, "q": ":name-asc"}


def test_tramits_procedure_parser_handles_sections(monkeypatch):
    content = (FIXTURES / "tramits-gv000484.html").read_text(encoding="utf-8")
    parsed = tramits._Page()
    parsed.feed(content)
    monkeypatch.setattr(
        tramits, "_page",
        lambda path, params=None: ("https://www.e-tramits.ad/tramits/a1-residencia-i-treball-autoritzacio-inicial/p/GV000484",
                                  content, parsed),
    )
    result = tramits.procedure(
        "https://www.e-tramits.ad/tramits/a1-residencia-i-treball-autoritzacio-inicial/p/GV000484"
    )
    assert result["code"] == "GV000484"
    assert result["title"] == "Example procedure"
    assert result["max_resolution"] == "60 days"
    assert result["online_available"] is False
    assert result["appointment_required"] is True


def test_tramits_list_all_uses_stable_sort_until_total(monkeypatch, tmp_path):
    pages = {
        0: [{"code": "GV000001", "title": "A", "url": "https://example.ad/a"},
            {"code": "GV000002", "title": "B", "url": "https://example.ad/b"}],
        1: [{"code": "GV000003", "title": "C", "url": "https://example.ad/c"}],
    }
    requested_pages = []

    def search_page(text, page, stable_sort=False):
        assert text == ""
        assert stable_sort is True
        requested_pages.append(page)
        return pages.get(page, []), 3

    monkeypatch.setattr(tramits, "_search_page", search_page)
    monkeypatch.setattr(tramits, "CACHE_PATH", tmp_path / "tramits.json")
    result = tramits.list_all(refresh=True)
    assert requested_pages == [0, 1]
    assert [item["code"] for item in result] == ["GV000001", "GV000002", "GV000003"]


def test_feed_parser_reads_saved_atom(monkeypatch):
    content = (FIXTURES / "consell-general-feed.xml").read_bytes()

    class Response:
        status_code = 200
        def raise_for_status(self):
            return None

        @property
        def content(self):
            return content

    monkeypatch.setattr(feeds.http, "get", lambda *args, **kwargs: Response())
    items = feeds.latest("consell-general")
    assert items and items[0]["title"]
    assert items[0]["url"]


def test_afa_aggregates_available_categories_after_timeout(monkeypatch):
    import requests

    class Response:
        content = (
            b"<rss><channel><item><title>Example item</title>"
            b"<link>https://example.ad/item</link></item></channel></rss>"
        )

        def raise_for_status(self):
            return None

    def get(url, **kwargs):
        if "educacio-financiera" in url:
            raise requests.Timeout("feed timed out")
        return Response()

    monkeypatch.setattr(feeds.http, "get", get)
    items = feeds.latest("afa")
    assert items
    assert items[0]["title"] == "Example item"
