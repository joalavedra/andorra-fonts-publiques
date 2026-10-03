from pathlib import Path

import pytest

from fonts_andorra.clients import govern

FIXTURES = Path(__file__).parent / "fixtures"


def test_govern_page_parses_title_description_and_liferay_sections(monkeypatch):
    html = (FIXTURES / "govern_passaports.html").read_text(encoding="utf-8")

    class Response:
        url = "https://www.govern.ad/ca/ministeris-i-secretaries-d-estat/ministeri-de-justicia-i-interior/passaports"
        text = html

        def raise_for_status(self):
            return None

    monkeypatch.setattr(govern.http, "get", lambda url: Response())
    result = govern.page(Response.url)

    assert result["title"] == "Passaports"
    assert "requisits" in result["description"].lower()
    assert result["lang"] == "ca"
    assert "49,31" in result["sections"]["Import"]
    assert "Prefooter" not in result["sections"]


def test_govern_page_rejects_non_govern_urls(monkeypatch):
    monkeypatch.setattr(govern.http, "get", lambda url: pytest.fail("unexpected request"))
    with pytest.raises(ValueError, match="https://www.govern.ad"):
        govern.page("https://example.com/ca/page")


def test_govern_parser_merges_duplicate_headings_and_keeps_nested_text_separate():
    parser = govern._Page()
    parser.feed("""<html lang="ca"><body>
      <div class="journal-content-article" data-analytics-asset-title="Parent">
        Before <script>hidden script</script>
        <div class="journal-content-article" data-analytics-asset-title="Child">inside</div>
        after
      </div>
      <div class="journal-content-article" data-analytics-asset-title="Parent">second</div>
      <div class="journal-content-article" data-analytics-asset-title="Empty"></div>
    </body></html>""")

    assert parser.sections == {"Child": "inside", "Parent": "Before after second"}


def test_govern_sitemap_excludes_news_by_default(monkeypatch):
    xml = b"""<?xml version="1.0"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url><loc>https://www.govern.ad/ca/tematiques/passaport</loc><lastmod>2025-01-01</lastmod></url>
      <url><loc>https://www.govern.ad/ca/w/news</loc><lastmod>2025-01-02</lastmod></url>
    </urlset>"""

    class Response:
        content = xml

        def raise_for_status(self):
            return None

    requested = []
    monkeypatch.setattr(govern.http, "get", lambda url: requested.append(url) or Response())

    assert govern.sitemap() == [{
        "url": "https://www.govern.ad/ca/tematiques/passaport",
        "lastmod": "2025-01-01",
    }]
    assert len(govern.sitemap(include_news=True)) == 2
    assert requested == ["https://www.govern.ad/ca/sitemap.xml"] * 2


def test_govern_sitemap_recovers_duplicate_empty_url_openers(monkeypatch):
    xml = b"""<?xml version="1.0"?>
    <urlset>
      <url><loc>https://www.govern.ad/ca/first</loc></url>
      <url>
      <url><loc>https://www.govern.ad/ca/second</loc></url>
    </urlset>"""

    class Response:
        content = xml

        def raise_for_status(self):
            return None

    monkeypatch.setattr(govern.http, "get", lambda url: Response())

    assert [item["url"] for item in govern.sitemap()] == [
        "https://www.govern.ad/ca/first",
        "https://www.govern.ad/ca/second",
    ]
