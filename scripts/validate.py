#!/usr/bin/env python3
"""Validate source fiches against the JSON schema and closed vocabularies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "sources"
SCHEMA_PATH = ROOT / "schema" / "source.schema.json"
VOCAB_PATH = ROOT / "schema" / "vocab.yaml"
ID_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def _matches_type(value, expected) -> bool:
    types = expected if isinstance(expected, list) else [expected]
    for kind in types:
        if kind == "null" and value is None:
            return True
        if kind == "object" and isinstance(value, dict):
            return True
        if kind == "array" and isinstance(value, list):
            return True
        if kind == "string" and isinstance(value, str):
            return True
        if kind == "integer" and isinstance(value, int) and not isinstance(value, bool):
            return True
        if kind == "number" and isinstance(value, (int, float)) and not isinstance(value, bool):
            return True
        if kind == "boolean" and isinstance(value, bool):
            return True
    return False


def _schema_errors(value, schema: dict, where: str) -> list[str]:
    errors = []
    if "type" in schema and not _matches_type(value, schema["type"]):
        return [f"{where}: expected {schema['type']}"]
    if isinstance(value, dict):
        for required in schema.get("required", []):
            if required not in value:
                errors.append(f"{where}: missing {required}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value.keys() - properties.keys():
                errors.append(f"{where}: unexpected property {key}")
        for key, child in properties.items():
            if key in value:
                errors.extend(_schema_errors(value[key], child, f"{where}.{key}"))
    elif isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{where}: fewer than {schema['minItems']} items")
        if len(value) > schema.get("maxItems", float("inf")):
            errors.append(f"{where}: more than {schema['maxItems']} items")
        if schema.get("uniqueItems") and len({json.dumps(item, sort_keys=True) for item in value}) != len(value):
            errors.append(f"{where}: duplicate items")
        if "items" in schema:
            for index, child_value in enumerate(value):
                errors.extend(_schema_errors(child_value, schema["items"], f"{where}[{index}]"))
    elif isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{where}: shorter than {schema['minLength']} characters")
        if len(value) > schema.get("maxLength", float("inf")):
            errors.append(f"{where}: longer than {schema['maxLength']} characters")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{where}: does not match {schema['pattern']}")
        if schema.get("format") == "uri" and value:
            parsed = urlparse(value)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                errors.append(f"{where}: expected HTTP(S) URI")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{where}: {value!r} is not one of {schema['enum']}")
    return errors


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    vocab = yaml.safe_load(VOCAB_PATH.read_text(encoding="utf-8"))
    files = sorted(SOURCE_DIR.glob("*.yaml"))
    errors = []
    by_id = {}
    for path in files:
        source = yaml.safe_load(path.read_text(encoding="utf-8"))
        errors.extend(_schema_errors(source, schema, path.name))
        source_id = source.get("id", "")
        if path.stem != source_id:
            errors.append(f"{path.name}: id does not match filename")
        if source_id in by_id:
            errors.append(f"{path.name}: duplicate source id {source_id}")
        by_id[source_id] = source
        for field in ("sector", "auth", "update", "status"):
            if source.get(field) not in vocab.get(field + "s", vocab.get(field, {})):
                errors.append(f"{path.name}: {field} value {source.get(field)!r} is outside vocabulary")
        for field in ("access", "formats", "quirks"):
            allowed = vocab.get(field, {})
            for value in source.get(field, []):
                if value not in allowed:
                    errors.append(f"{path.name}: {field} value {value!r} is outside vocabulary")
    for path in files:
        source = yaml.safe_load(path.read_text(encoding="utf-8"))
        for related in source.get("related", []):
            if related not in by_id:
                errors.append(f"{path.name}: related id {related!r} does not exist")
    dead = yaml.safe_load((ROOT / "indices" / "dead-routes.yaml").read_text(encoding="utf-8"))
    if dead.get("checked") != "2026-10-02":
        errors.append("indices/dead-routes.yaml: checked date must be 2026-10-02")
    for entry in dead.get("domains", []):
        if not re.fullmatch(r"[a-z0-9.-]+", str(entry.get("domain", ""))):
            errors.append(f"indices/dead-routes.yaml: invalid domain {entry.get('domain')!r}")
        if entry.get("status") != "unresolved":
            errors.append(f"indices/dead-routes.yaml: unexpected status for {entry.get('domain')}")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"Validated {len(files)} source fiches and {len(dead.get('domains', []))} unresolved domains.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
