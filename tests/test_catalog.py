from fonts_andorra import catalog


def test_catalog_search_ignores_accents():
    source = {
        "id": "estadistica-api",
        "name": "Andorra Department of Estadística",
        "org": "Departament d'Estadística",
        "sector": "statistics",
        "tags": ["time-series"],
        "summary": "Search public tables",
        "base_url": "https://example.ad/api",
        "status": "active",
    }
    result = catalog.search("estadistica", catalog={"sources": [source]})
    assert result == [source]
