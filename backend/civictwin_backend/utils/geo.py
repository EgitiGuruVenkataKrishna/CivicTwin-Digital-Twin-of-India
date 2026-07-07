"""Geospatial utility helpers for CivicTwin.

Provides lightweight coordinate / geometry conversions used across the
backend.  These helpers intentionally avoid heavy geo libraries and
produce WKT strings suitable for direct use in PostGIS queries.
"""

from __future__ import annotations

import json
from typing import Any

# ── Hyderabad pilot city bounding box (WGS-84) ─────────────────────────

HYDERABAD_BBOX: dict[str, float] = {
    "west": 78.2,
    "south": 17.2,
    "east": 78.6,
    "north": 17.55,
}


# ── Conversion helpers ──────────────────────────────────────────────────


def bbox_to_polygon(bbox: dict[str, float]) -> str:
    """Convert a ``{west, south, east, north}`` dict to a WKT POLYGON.

    The resulting polygon follows the exterior-ring convention
    (counter-clockwise) and is in SRID 4326.
    """
    w, s, e, n = bbox["west"], bbox["south"], bbox["east"], bbox["north"]
    return (
        f"POLYGON(({w} {s}, {e} {s}, {e} {n}, {w} {n}, {w} {s}))"
    )


def geojson_to_wkt(geojson: dict[str, Any]) -> str:
    """Convert a GeoJSON geometry dict to its WKT representation.

    Supports ``Polygon`` and ``Point`` geometry types – the two types
    used by CivicTwin zone and observation models.
    """
    geom_type = geojson.get("type", "")
    coordinates = geojson.get("coordinates")

    if geom_type == "Point":
        lon, lat = coordinates
        return f"POINT({lon} {lat})"

    if geom_type == "Polygon":
        rings: list[str] = []
        for ring in coordinates:
            coords_str = ", ".join(f"{lon} {lat}" for lon, lat in ring)
            rings.append(f"({coords_str})")
        return f"POLYGON({', '.join(rings)})"

    raise ValueError(f"Unsupported GeoJSON geometry type: {geom_type}")


def point_to_wkt(lat: float, lon: float) -> str:
    """Return a WKT ``POINT(lon lat)`` string."""
    return f"POINT({lon} {lat})"


def validate_bbox(bbox: dict[str, float]) -> bool:
    """Check that a bounding-box dict has valid WGS-84 coordinate ranges.

    Returns ``True`` when:
    * west < east
    * south < north
    * longitude ∈ [-180, 180]
    * latitude  ∈ [-90, 90]
    """
    try:
        w, s, e, n = bbox["west"], bbox["south"], bbox["east"], bbox["north"]
    except KeyError:
        return False

    if not (-180.0 <= w <= 180.0 and -180.0 <= e <= 180.0):
        return False
    if not (-90.0 <= s <= 90.0 and -90.0 <= n <= 90.0):
        return False
    if w >= e or s >= n:
        return False

    return True
