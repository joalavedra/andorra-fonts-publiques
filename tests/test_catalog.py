import json

from fonts_andorra import catalog


def test_load_catalog_prefers_explicit_path(tmp_path, monkeypatch):
    root = tmp_path / "root"
    root.mkdir()
    (root / "catalog.json").write_text(json.dumps({"sources": [{"id": "root"}]}))
    explicit = tmp_path / "explicit.json"
    explicit.write_text(json.dumps({"sources": [{"id": "explicit"}]}))
    monkeypatch.setattr(catalog, "ROOT", root)

    assert catalog.load_catalog(explicit)["sources"] == [{"id": "explicit"}]


def test_load_catalog_prefers_repository_catalog_to_package_copy(tmp_path, monkeypatch):
    (tmp_path / "catalog.json").write_text(json.dumps({"sources": [{"id": "repository"}]}))
    monkeypatch.setattr(catalog, "ROOT", tmp_path)

    assert catalog.load_catalog()["sources"] == [{"id": "repository"}]


def test_load_catalog_uses_package_copy_when_repository_catalog_is_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(catalog, "ROOT", tmp_path)

    loaded = catalog.load_catalog()

    assert len(loaded["sources"]) >= 11
    assert catalog.source("bopa", loaded) is not None


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
