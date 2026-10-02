#!/usr/bin/env python3
"""Build the compact JSON and text catalog outputs from source fiches."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "sources"
README = ROOT / "README.md"
START = "<!-- AUTO:SOURCES -->"
END = "<!-- /AUTO:SOURCES -->"


def load_sources() -> list[dict]:
    return [
        yaml.safe_load(path.read_text(encoding="utf-8"))
        for path in sorted(SOURCE_DIR.glob("*.yaml"))
    ]


def source_table(sources: list[dict]) -> str:
    rows = [
        "| ID | Source | Sector | Access | Licence |",
        "|---|---|---|---|---|",
    ]
    for source in sources:
        license_text = source["license"].replace("|", "\\|")
        rows.append(
            f"| `{source['id']}` | [{source['name']}]({source['base_url']}) | "
            f"{source['sector']} | {', '.join(source['access'])} | {license_text} |"
        )
    return "\n".join(rows)


def main() -> None:
    sources = load_sources()
    dead_routes = yaml.safe_load((ROOT / "indices" / "dead-routes.yaml").read_text(encoding="utf-8"))
    (ROOT / "catalog.json").write_text(
        json.dumps({"sources": sources, "dead_routes": dead_routes}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    short_lines = [
        "# Andorra public sources",
        "",
        "Educational catalog; live endpoints, reuse notes, known traps and example calls.",
        "",
        "| ID | Source | Sector | Summary |",
        "|---|---|---|---|",
    ]
    full_lines = ["# Andorra public sources — full catalog", ""]
    for source in sources:
        short_lines.append(
            f"| `{source['id']}` | {source['name']} | {source['sector']} | {source['summary']} |"
        )
        full_lines.extend([
            f"## {source['name']} (`{source['id']}`)",
            "",
            f"- Organization: {source['org']}",
            f"- Summary: {source['summary']}",
            f"- Access: {', '.join(source['access'])}",
            f"- Authentication: {source['auth']}",
            f"- Licence: {source['license']}",
            f"- Base URL: {source['base_url']}",
            f"- Verified: {source['verified'] or 'not rechecked'}",
            "",
            "### Endpoints",
            "",
        ])
        for endpoint in source["endpoints"]:
            full_lines.extend([
                f"- `{endpoint['method']} {endpoint['path']}` — {endpoint['desc']}",
                f"  Example: `{endpoint['example']}`",
                f"  Returns: {endpoint['returns']}",
            ])
        full_lines.extend(["", "### Alerts and gotchas", ""])
        full_lines.extend(f"- {item}" for item in source["alerts"] + source["gotchas"])
        full_lines.extend(["", ""])
    (ROOT / "llms.txt").write_text("\n".join(short_lines) + "\n", encoding="utf-8")
    full_text = "\n".join(full_lines).rstrip("\n") + "\n"
    (ROOT / "llms-full.txt").write_text(full_text, encoding="utf-8")
    if README.exists():
        readme = README.read_text(encoding="utf-8")
        before, marker, rest = readme.partition(START)
        if marker:
            _, end_marker, after = rest.partition(END)
            if end_marker:
                readme = before + START + "\n" + source_table(sources) + "\n" + END + after
                README.write_text(readme, encoding="utf-8")
    print(f"Built catalog and text indexes for {len(sources)} sources.")


if __name__ == "__main__":
    main()
