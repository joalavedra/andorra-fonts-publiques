"""Curated ArcGIS REST layer queries with complete offset paging."""

from __future__ import annotations

from datetime import datetime, timezone

from fonts_andorra.clients import http

ROOT = "https://sig.govern.ad/server/rest/services"


class ArcgisError(RuntimeError):
    """ArcGIS error returned in a JSON response body."""


WHITELIST = {
    "carburants_stations": {"service": f"{ROOT}/CARBURANTS/CARBURANTS/FeatureServer", "layer_id": 0},
    "carburants_prices": {"service": f"{ROOT}/CARBURANTS/CARBURANTS/FeatureServer", "layer_id": 1},
    "aadt": {"service": f"{ROOT}/Hosted/IMD_Intensitat_Mitjana_Di%C3%A0ria/FeatureServer", "name": "IMD (Intensitat Mitjana Diària)"},
    "weather_stations": {"service": f"{ROOT}/Hosted/Estacions_meteorol%C3%B2giques_Andorra/FeatureServer", "name": "Estacions meteo Andorra"},
    "streets": {"service": f"{ROOT}/Hosted/Carrerer_Andorra/FeatureServer", "name": "Carrerer_Andorra"},
    "population": {"service": f"{ROOT}/Hosted/Poblaci%C3%B3_2010_2021/FeatureServer", "name": "Població_2010_25"},
    "tourism_pois": {"service": f"{ROOT}/Hosted/Mapa_POIS_turisme_Andorra_WFL1/FeatureServer", "name": "POIS_Turisme_Andorra"},
    "bus_lines": {"service": f"{ROOT}/Hosted/linies_bus_2025/FeatureServer", "name": "Línies Coopalsa juliol 2025"},
    "parishes": {"service": f"{ROOT}/Hosted/limits_parroquials/FeatureServer", "name": "limit_parroquies"},
}


def _json(url: str, params: dict | None = None) -> dict:
    response = http.get(url, params={"f": "json", **(params or {})})
    response.raise_for_status()
    payload = response.json()
    if isinstance(payload, dict) and "error" in payload:
        error = payload["error"]
        details = " ".join(error.get("details") or [])
        raise ArcgisError(f"{error.get('code')} {error.get('message', '')} {details}".strip())
    return payload


def layers(service_url: str) -> list[dict]:
    service = _json(service_url.rstrip("/"))
    if "layers" not in service:
        raise ArcgisError("ArcGIS service response has no layers list")
    return service["layers"]


def resolve(key: str) -> str:
    if key not in WHITELIST:
        raise KeyError(f"Unknown curated ArcGIS layer: {key}")
    config = WHITELIST[key]
    service = config["service"]
    layer_id = config.get("layer_id")
    if layer_id is None:
        found = next((layer for layer in layers(service) if layer.get("name") == config["name"]), None)
        if found is None:
            raise ArcgisError(f"Layer {config['name']!r} not found in {service}")
        layer_id = found["id"]
    return f"{service.rstrip('/')}/{layer_id}"


def _metadata(layer_url: str) -> dict:
    return _json(layer_url.rstrip("/"))


def _iso_dates(attributes: dict, metadata: dict) -> dict:
    for field in metadata.get("fields", []):
        name = field.get("name")
        value = attributes.get(name)
        if field.get("type") == "esriFieldTypeDate" and isinstance(value, (int, float)):
            attributes[name] = datetime.fromtimestamp(value / 1000, tz=timezone.utc).isoformat()
    return attributes


def query(layer_url: str, where: str = "1=1", out_fields: str = "*", limit: int | None = None) -> list[dict]:
    layer_url = layer_url.rstrip("/")
    metadata = _metadata(layer_url)
    page_size = int(metadata.get("maxRecordCount") or 1000)
    results: list[dict] = []
    offset = 0
    while limit is None or len(results) < limit:
        params = {
            "where": where,
            "outFields": out_fields,
            "returnGeometry": "true",
            "resultOffset": offset,
            "resultRecordCount": min(page_size, limit - len(results)) if limit is not None else page_size,
            "orderByFields": metadata.get("objectIdField") or "",
        }
        if not params["orderByFields"]:
            oid = next((field["name"] for field in metadata.get("fields", [])
                        if field.get("type") == "esriFieldTypeOID"), None)
            if oid:
                params["orderByFields"] = oid
            else:
                params.pop("orderByFields")
        payload = _json(f"{layer_url}/query", params=params)
        features = payload.get("features", [])
        for feature in features:
            if isinstance(feature, dict) and isinstance(feature.get("attributes"), dict):
                _iso_dates(feature["attributes"], metadata)
            results.append(feature)
        offset += len(features)
        if not features or not payload.get("exceededTransferLimit") or (limit is not None and len(results) >= limit):
            break
    return results


def count(layer_url: str, where: str = "1=1") -> int:
    payload = _json(f"{layer_url.rstrip('/')}/query", params={"where": where, "returnCountOnly": "true"})
    return int(payload["count"])
