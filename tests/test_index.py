from fonts_andorra import index


def test_bm25_search_uses_title_headings_and_source_filter(monkeypatch):
    items = [
        {
            "source": "govern.ad",
            "id": "/ca/tematiques/passaport",
            "title": "Passaports",
            "url": "https://www.govern.ad/ca/tematiques/passaport/renovacio",
            "headings": ["Import", "Renovació"],
        },
        {
            "source": "e-tramits",
            "id": "GV000001",
            "title": "Passaport",
            "url": "https://www.e-tramits.ad/tramits/passaport/p/GV000001",
            "headings": [],
        },
    ]
    monkeypatch.setattr(index, "_load_index", lambda: {"items": items})

    results = index.search("passaports renovació", source="govern.ad")

    assert [item["source"] for item in results] == ["govern.ad"]
    assert results[0]["id"] == "/ca/tematiques/passaport"
    assert results[0]["score"] > 0
    assert index.search("tematiques", source="govern.ad") == []
    assert index.search("the and with", source="govern.ad") == []


def test_bm25_ties_are_broken_by_url(monkeypatch):
    items = [
        {
            "source": "govern.ad",
            "id": "two",
            "title": "Passport information",
            "url": "https://www.govern.ad/ca/second",
            "headings": [],
        },
        {
            "source": "govern.ad",
            "id": "one",
            "title": "Passport information",
            "url": "https://www.govern.ad/ca/first",
            "headings": [],
        },
    ]
    monkeypatch.setattr(index, "_load_index", lambda: {"items": items})

    results = index.search("passport information")

    assert [item["url"] for item in results] == [
        "https://www.govern.ad/ca/first",
        "https://www.govern.ad/ca/second",
    ]
