"""Check essential functionality from an installed wheel."""

from importlib.metadata import version

from fonts_andorra import __version__, catalog, index, mcp_server


def main() -> None:
    loaded = catalog.load_catalog()
    assert len(loaded.get("sources", [])) >= 11
    assert catalog.source("bopa", loaded) is not None
    assert index.search("passaport", source="govern.ad")
    assert mcp_server.server is not None
    assert version("fonts-andorra") == __version__
    print("Installed wheel checks passed.")


if __name__ == "__main__":
    main()
