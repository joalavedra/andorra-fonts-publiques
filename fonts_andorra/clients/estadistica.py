"""Andorran statistics API and JSON-stat 2.0 parser."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from itertools import product

from fonts_andorra.clients import http

BASE = "https://sig.govern.ad/SIGDDE.Public/estadistiquesdades/api"


def search(text: str, language: str = "ca") -> list[dict]:
    if not text.strip():
        raise ValueError("text must not be empty")
    response = http.get(f"{BASE}/searchDivision", params={"text": text, "language": language})
    response.raise_for_status()
    return response.json()


def topics(language: str = "ca"):
    response = http.post(
        "https://sig.govern.ad/SIGDDE.Public/Inici/GetAgrupacionsByNivell",
        json={"Nivells": [1, 2, 3], "Idioma": language},
    )
    response.raise_for_status()
    return response.json()


def _label(dimension: dict, code: str) -> str:
    category = dimension.get("category", {})
    labels = category.get("label", {})
    return str(labels.get(str(code), code)) if isinstance(labels, dict) else str(code)


def _position(dimension: dict, code: str) -> int:
    index = dimension.get("category", {}).get("index", {})
    if isinstance(index, list):
        return index.index(code)
    return int(index.get(str(code), 0))


def _scale_value(dataset: dict, codes: dict[str, str], value):
    if value is None:
        return None
    dimensions = dataset.get("dimension", {})
    try:
        number = Decimal(str(value))
    except InvalidOperation:
        return value
    decimals = None
    scale = Decimal(1)
    for dimension_id, code in codes.items():
        dimension = dimensions.get(dimension_id, {})
        label = _label(dimension, code).lower()
        if dimension_id.upper() == "DECIMALS":
            try:
                decimals = int(code)
            except (TypeError, ValueError):
                try:
                    decimals = int(label)
                except ValueError:
                    decimals = None
        elif dimension_id.upper() == "IDESCALA":
            try:
                scale_code = int(code)
            except (TypeError, ValueError):
                scale_code = 0
            # Common scale labels are explicit; IDs otherwise represent powers of ten.
            if "milió" in label or "million" in label:
                scale = Decimal(1_000_000)
            elif "miler" in label or "thousand" in label or "miles" in label:
                scale = Decimal(1_000)
            elif "cent" in label or "hundred" in label:
                scale = Decimal(100)
            elif "unitat" in label or "unidad" in label or "unite" in label or "unit" in label:
                scale = Decimal(1)
            else:
                scale = Decimal(10) ** scale_code
    number *= scale
    if decimals is not None:
        number = number.quantize(Decimal(1).scaleb(-decimals))
    return int(number) if number == number.to_integral_value() else float(number)


def parse_jsonstat(dataset: dict) -> list[dict]:
    dim_ids = dataset.get("id") or []
    sizes = dataset.get("size") or []
    dimensions = dataset.get("dimension") or {}
    if not dim_ids or len(dim_ids) != len(sizes):
        return []
    codes_by_dim = []
    for dim_id in dim_ids:
        categories = dimensions.get(dim_id, {}).get("category", {}).get("index", {})
        codes = list(categories.keys()) if isinstance(categories, dict) else list(categories)
        codes.sort(key=lambda code: _position(dimensions.get(dim_id, {}), code))
        codes_by_dim.append(codes)
    values = dataset.get("value", [])
    rows: list[dict] = []
    for coordinates in product(*(range(size) for size in sizes)):
        flat_index = 0
        for coordinate, size in zip(coordinates, sizes):
            flat_index = flat_index * size + coordinate
        raw = values.get(str(flat_index)) if isinstance(values, dict) else values[flat_index] if flat_index < len(values) else None
        codes = {dim_ids[index]: codes_by_dim[index][coordinate]
                 for index, coordinate in enumerate(coordinates)}
        time_dim = next((key for key in dim_ids if dimensions.get(key, {}).get("role") == "time"), None)
        if time_dim is None:
            time_dim = next((key for key in dim_ids if key.lower() in {
                "time", "time_period", "period", "periode", "any",
            }), dim_ids[0])
        period_code = codes[time_dim]
        series = [key for key in dim_ids if key != time_dim and key.upper() not in {"DECIMALS", "IDESCALA"}]
        series_code = "|".join(str(codes[key]) for key in series)
        series_label = " · ".join(_label(dimensions.get(key, {}), codes[key]) for key in series)
        rows.append({
            "series_code": series_code or str(dataset.get("label", "")),
            "series_label": series_label or str(dataset.get("label", "")),
            "period": str(period_code),
            "value": _scale_value(dataset, codes, raw),
        })
    return rows


def data(id_division: int | str, start: str | None = None, end: str | None = None,
         language: str = "ca", variation: str = "Cap") -> list[dict]:
    response = http.get(f"{BASE}/data", params={
        "file": "json-stat",
        "idDivision": id_division,
        "language": language,
        "variation": variation,
        "startDate": start or "1900",
        "endDate": end or "2100",
    })
    response.raise_for_status()
    return parse_jsonstat(response.json())
