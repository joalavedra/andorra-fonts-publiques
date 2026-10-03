#!/usr/bin/env python3
"""Run the requested one-shot live smoke checks and save public response fixtures."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path("/home/ubuntu/repos/andorra-fonts-publiques-smoke.txt")
FIXTURES = ROOT / "tests" / "fixtures"


def _save(name: str, content: bytes) -> None:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    (FIXTURES / name).write_bytes(content)


def _capture(response, *args, **kwargs):
    parsed = urlparse(response.url)
    query = parse_qs(parsed.query)
    host = parsed.hostname or ""
    if host == "bopaazurefunctions.azurewebsites.net" and parsed.path.endswith("GetPaginatedDocuments2Indexes"):
        try:
            payload = response.json()
            if isinstance(payload, list):
                payload = {"items": payload}
            key = next((name for name in ("results", "documents", "items", "value", "paginatedDocuments")
                        if isinstance(payload, dict) and isinstance(payload.get(name), list)), None)
            if key:
                fields = (
                    "nomDocument", "metadata_storage_name", "dataPublicacioButlleti",
                    "dataPublicacio", "pub_date", "numButlleti", "numBOPA", "bulletin",
                    "anyButlleti", "organisme", "tema", "metadata_storage_path", "fileType",
                )
                def document_fields(item):
                    document = item.get("document") if isinstance(item, dict) else None
                    document = document if isinstance(document, dict) else item
                    return {name: document[name] for name in fields if isinstance(document, dict) and name in document}

                payload = {
                    **{name: payload[name] for name in ("totalCount", "count") if name in payload},
                    key: [{"document": document_fields(item)} for item in payload[key][:3]
                          if isinstance(item, dict)] if key == "paginatedDocuments" else [
                              document_fields(item) for item in payload[key][:3] if isinstance(item, dict)
                          ],
                }
                _save("bopa-search.json", json.dumps(payload, ensure_ascii=False).encode("utf-8"))
        except (TypeError, ValueError):
            pass
    if (parsed.path.endswith("/estadistiquesdades/api/data") and query.get("idDivision") == ["1070"]
            and query.get("file") == ["json-stat"]
            and response.status_code == 200 and response.content):
        stats_payload = json.dumps(response.json(), ensure_ascii=False, indent=2) + "\n"
        _save("stats-1070.json", stats_payload.encode("utf-8"))
    if host == "www.consellgeneral.ad" and parsed.path.lower() == "/rss":
        _save("consell-general-feed.xml", _sanitize_feed(response.content))
    if host == "www.afa.ad" and parsed.path.lower() == "/rss":
        _save("afa-feed.xml", _sanitize_feed(response.content))
    return response


def _sanitize_feed(content: bytes) -> bytes:
    root = ET.fromstring(content)

    def local_name(tag):
        return tag.rsplit("}", 1)[-1].lower()

    def keep_one_entry(parent):
        entries = [child for child in list(parent) if local_name(child.tag) in {"item", "entry", "li"}]
        for entry in entries[1:]:
            parent.remove(entry)
        for child in list(parent):
            keep_one_entry(child)

    keep_one_entry(root)
    for element in root.iter():
        field = local_name(element.tag)
        if field in {"title", "description", "summary", "content", "encoded", "link", "guid", "id"}:
            element.text = "Example feed item."
        elif field in {"pubdate", "published", "updated", "date"}:
            element.text = "2026-10-02T00:00:00Z"
        elif field in {"creator", "author", "name"}:
            element.text = "Example publisher"
        for attribute in list(element.attrib):
            if attribute.rsplit("}", 1)[-1].lower() in {"about", "href", "resource", "uri"}:
                element.attrib[attribute] = "https://example.ad/item"
        if element.text is not None and not element.text.strip():
            element.text = None
        if element.tail is not None and not element.tail.strip():
            element.tail = None
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run live source smoke checks.")
    parser.add_argument("--out", type=Path, default=OUTPUT, help="Path for the smoke report.")
    parser.add_argument("--no-fixtures", action="store_true", help="Do not write response fixtures.")
    args = parser.parse_args(argv)

    sys.path.insert(0, str(ROOT))
    from fonts_andorra.clients import arcgis, bopa, estadistica, feeds, http, tramits

    if not args.no_fixtures:
        http.session.hooks.setdefault("response", []).append(_capture)
    lines = []
    errors = []

    def run(label, callback):
        try:
            value = callback()
            lines.append(f"{label}: {value}")
            return value
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{label}: {type(exc).__name__}: {exc}")
            lines.append(f"ERROR {label}: {type(exc).__name__}: {exc}")
            return None

    run("bopa.search(habitatge) total", lambda: bopa.search("habitatge")["total"])
    run("bopa.bulletin(2026, 100) count", lambda: len(bopa.bulletin(2026, 100)))
    stats_rows = run("estadistica.data(1070) rows and last period", lambda: estadistica.data(1070))
    if stats_rows is not None:
        summary = {"rows": len(stats_rows), "last_period": max(
            (row["period"] for row in stats_rows), default=None
        )}
        lines[-1] = "estadistica.data(1070) rows and last period: " + json.dumps(summary)
    for key in arcgis.WHITELIST:
        def count_layer(key=key):
            url = arcgis.resolve(key)
            metadata = arcgis._metadata(url)
            return {"url": url, "name": metadata.get("name"), "count": arcgis.count(url)}
        run(f"ArcGIS {key}", count_layer)
    run("tramits.search(vehicle) reported total", lambda: tramits._search_page("vehicle", 0)[1])
    run("tramits.search(vehicle) page size", lambda: len(tramits.search("vehicle")))
    run("tramits.search(taxi) codes", lambda: [item["code"] for item in tramits.search("taxi")])
    run("tramits.list_all count", lambda: len(tramits.list_all(refresh=True)))
    procedure = run("tramits.procedure(GV000484) fields", lambda: tramits.procedure("GV000484"))
    if procedure:
        lines[-1] = "tramits.procedure(GV000484) fields: " + json.dumps({
            "code": procedure["code"],
            "title": procedure["title"],
            "url": procedure["url"],
            "section_headings": list(procedure["sections"]),
            "price": procedure["price"],
            "max_resolution": procedure["max_resolution"],
            "online_available": procedure["online_available"],
            "appointment_required": procedure["appointment_required"],
        }, ensure_ascii=False)
    for lang in ("es", "fr"):
        run(f"tramits.GV000484 {lang} URL", lambda lang=lang: tramits.procedure("GV000484", lang)["url"])
    for feed_key in ("consell-general", "afa"):
        items = run(f"feed {feed_key}", lambda feed_key=feed_key: feeds.latest(feed_key, 3))
        if items:
            lines[-1] = f"feed {feed_key}: " + json.dumps({
                "count": len(items),
                "items": [{
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "date": item.get("date"),
                    "summary": (item.get("summary") or "")[:200],
                } for item in items],
            }, ensure_ascii=False)

    if stats_rows is not None:
        run("statistics JSON-stat vs CSV values", lambda: _check_csv(estadistica, http, stats_rows))
    if args.no_fixtures:
        lines.append("fixture capture: SKIPPED (--no-fixtures)")
    else:
        lines.append(f"fixture files captured: {sorted(path.name for path in FIXTURES.glob('*'))}")
    if os.environ.get("GEMINI_API_KEY"):
        try:
            result = subprocess.run(
                [sys.executable, "-m", "fonts_andorra.assistant.cli",
                 "Quant triga l'autorització inicial de residència i treball?", "--json"],
                cwd=ROOT, text=True, capture_output=True, timeout=150, check=False,
            )
            if result.returncode:
                raise RuntimeError(f"assistant exit {result.returncode}")
            answer = json.loads(result.stdout)
            lines.append("fonts-andorra-ask: " + json.dumps(answer, ensure_ascii=False))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"fonts-andorra-ask: {type(exc).__name__}: {exc}")
            lines.append(f"ERROR fonts-andorra-ask: {type(exc).__name__}: {exc}")
    else:
        lines.append("fonts-andorra-ask: SKIPPED (GEMINI_API_KEY is not set)")
    if errors:
        lines = [line for line in lines if not line.startswith("Failures:")]
        lines.append("Failures: " + " | ".join(errors))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Saved smoke output to {args.out}")
    print("\n".join(lines))
    return 1 if errors else 0


def _check_csv(estadistica, http, json_rows):
    import csv
    import re
    from collections import defaultdict
    from decimal import Decimal, InvalidOperation
    from io import StringIO

    response = http.get(f"{estadistica.BASE}/data", params={
        "file": "csv", "idDivision": 1070, "language": "ca", "variation": "Cap",
        "startDate": "1900", "endDate": "2100",
    })
    response.raise_for_status()
    rows = list(csv.reader(StringIO(response.text.lstrip("\ufeff")), delimiter=";"))
    if len(rows) < 2:
        raise AssertionError("Statistics CSV export has no data rows")
    headers = [cell.strip() for cell in rows[0]]
    period_columns = {
        header.replace("/", "-"): index for index, header in enumerate(headers)
        if re.fullmatch(r"\d{4}(?:/\d{2})?", header)
    }
    if not period_columns:
        raise AssertionError(f"No period columns found in CSV headers: {headers[:12]}")

    def number(value):
        value = value.strip().replace("\u00a0", "").replace(" ", "")
        if not value or value in {"-", ".."}:
            return None
        if "," in value:
            value = value.replace(".", "").replace(",", ".")
        try:
            return Decimal(value)
        except InvalidOperation:
            return None

    csv_values = defaultdict(set)
    for row in rows[1:]:
        for period, index in period_columns.items():
            if index < len(row):
                value = number(row[index])
                if value is not None:
                    csv_values[period].add(value)
    json_values = defaultdict(set)
    for row in json_rows:
        value = row.get("value")
        if value is not None:
            json_values[row["period"]].add(Decimal(str(value)))
    compared_periods = sorted(set(csv_values) & set(json_values))
    if not compared_periods:
        raise AssertionError("CSV and JSON-stat have no overlapping non-empty periods")
    mismatches = [
        period for period in compared_periods
        if csv_values[period] != json_values[period]
    ]
    if mismatches:
        period = mismatches[0]
        raise AssertionError(
            f"CSV and JSON-stat differ at {period}: "
            f"CSV={sorted(csv_values[period])[:5]}, JSON-stat={sorted(json_values[period])[:5]}"
        )
    return {
        "status": response.status_code,
        "csv_data_rows": len(rows) - 1,
        "matched_periods": len(compared_periods),
        "sample_period": compared_periods[-1],
        "values_at_sample_period": len(csv_values[compared_periods[-1]]),
    }


if __name__ == "__main__":
    raise SystemExit(main())
