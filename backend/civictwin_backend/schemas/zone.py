"""Zone schemas for CivicTwin.

Defines Pydantic v2 models for creating, updating, and reading urban zones
(residential, commercial, industrial, green_space, water_body) used in the
Hyderabad pilot city digital twin.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

ZONE_TYPES = Literal[
    "residential",
    "commercial",
    "industrial",
    "green_space",
    "water_body",
]


class ZoneCreate(BaseModel):
    """Payload for creating a new zone."""

    name: str
    zone_type: ZONE_TYPES
    geojson: dict  # GeoJSON Polygon geometry
    properties: dict | None = None


class ZoneUpdate(BaseModel):
    """Partial-update payload for an existing zone."""

    name: str | None = None
    zone_type: ZONE_TYPES | None = None
    properties: dict | None = None


class ZoneOut(BaseModel):
    """Zone representation returned to the client."""

    id: UUID
    name: str
    zone_type: str
    geojson: dict
    area_sqkm: float | None = None
    properties: dict | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
