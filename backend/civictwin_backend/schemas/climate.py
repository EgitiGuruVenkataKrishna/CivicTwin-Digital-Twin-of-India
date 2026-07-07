"""Climate data schemas for CivicTwin.

Defines Pydantic v2 models for climate observations, spatial bounding-box
queries, snapshot responses, and timeseries endpoints.  All models target
the Hyderabad pilot city and are consumed by the /api/v1/climate router.
"""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


# ── Spatial primitives ──────────────────────────────────────────────────


class BBox(BaseModel):
    """Axis-aligned bounding box in WGS-84 degrees."""

    west: float
    south: float
    east: float
    north: float


# ── Snapshot (spatial window query) ─────────────────────────────────────


class ClimateSnapshotRequest(BaseModel):
    """Parameters for a spatial-window climate query."""

    bbox: BBox
    dataset: str | None = None
    timestamp: datetime | None = None


class ClimateObservationOut(BaseModel):
    """Single climate observation returned to the client."""

    id: UUID
    dataset: str
    observed_at: datetime
    lat: float
    lon: float
    properties: dict
    grid_cell_id: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ClimateSnapshotResponse(BaseModel):
    """Paginated set of observations within a bounding box."""

    observations: list[ClimateObservationOut]
    count: int
    bbox: BBox
    queried_at: datetime


# ── Timeseries ──────────────────────────────────────────────────────────


class TimeseriesRequest(BaseModel):
    """Request parameters for a single-point timeseries extraction."""

    lat: float
    lon: float
    dataset: str
    start_date: date
    end_date: date


class TimeseriesPoint(BaseModel):
    """One point in a timeseries."""

    observed_at: datetime
    value: float
    uncertainty: float | None = None


class TimeseriesResponse(BaseModel):
    """Full timeseries response for a location + dataset."""

    dataset: str
    location: dict  # {"lat": ..., "lon": ...}
    points: list[TimeseriesPoint]
    count: int
