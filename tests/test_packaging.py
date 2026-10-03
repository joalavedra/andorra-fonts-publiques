import json
import re
from pathlib import Path

from fonts_andorra import __version__

ROOT = Path(__file__).resolve().parents[1]


def test_server_metadata_matches_package_and_readme():
    server = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    name_match = re.search(r"<!-- mcp-name: ([^ ]+) -->", readme)

    assert name_match is not None
    assert server["version"] == __version__
    assert server["packages"][0]["version"] == __version__
    assert server["name"] == name_match.group(1)
    assert len(server["description"]) <= 100
