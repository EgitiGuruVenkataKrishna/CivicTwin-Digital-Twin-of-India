"""Climate data router for CivicTwin.

Provides endpoints for spatial-window snapshots, single-point timeseries,
and latest-observation-per-dataset queries over Hyderabad climate data.

Prefix is intentionally empty — ``main.py`` mounts this router under
``/api/v1/climate``.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from civictwin_backend.database import get_db
from civictwin_backend.schemas.climate import (
    BBox,
    ClimateObservationOut,
    ClimateSnapshotResponse,
    TimeseriesPoint,
    TimeseriesResponse,
)
from civictwin_backend.services import climate_service
from civictwin_backend.utils.geo import HYDERABAD_BBOX

router = APIRouter()


# ── Snapshot ────────────────────────────────────────────────────────────


@router.get("/snapshot", response_model=ClimateSnapshotResponse)
async def get_snapshot(
    west: float = Query(..., description="Western longitude bound"),
    south: float = Query(..., description="Southern latitude bound"),
    east: float = Query(..., description="Eastern longitude bound"),
    north: float = Query(..., description="Northern latitude bound"),
    dataset: str | None = Query(None, description="Filter by dataset name"),
    limit: int = Query(1000, ge=1, le=10_000, description="Max observations"),
    db: AsyncSession = Depends(get_db),
) -> ClimateSnapshotResponse:
    """Return climate observations within a bounding box."""
    bbox_dict = {"west": west, "south": south, "east": east, "north": north}
    observations = await climate_service.get_snapshot(
        db, bbox_dict, dataset=dataset, limit=limit,
    )

    return ClimateSnapshotResponse(
        observations=[ClimateObservationOut.model_validate(o) for o in observations],
        count=len(observations),
        bbox=BBox(**bbox_dict),
        queried_at=datetime.now(timezone.utc),
    )


# ── Timeseries ──────────────────────────────────────────────────────────


@router.get("/timeseries", response_model=TimeseriesResponse)
async def get_timeseries(
    lat: float = Query(..., description="Latitude of query point"),
    lon: float = Query(..., description="Longitude of query point"),
    dataset: str = Query(..., description="Dataset name"),
    start_date: date = Query(..., description="Start date (inclusive)"),
    end_date: date = Query(..., description="End date (inclusive)"),
    db: AsyncSession = Depends(get_db),
) -> TimeseriesResponse:
    """Return a timeseries for the nearest observation point."""
    observations = await climate_service.get_timeseries(
        db, lat, lon, dataset, start_date, end_date,
    )

    points = [
        TimeseriesPoint(
            observed_at=o.observed_at,
            value=o.properties.get("value", 0.0),
            uncertainty=o.properties.get("uncertainty"),
        )
        for o in observations
    ]

    return TimeseriesResponse(
        dataset=dataset,
        location={"lat": lat, "lon": lon},
        points=points,
        count=len(points),
    )


# ── Latest per dataset ─────────────────────────────────────────────────


@router.get("/latest", response_model=list[ClimateObservationOut])
async def get_latest(
    db: AsyncSession = Depends(get_db),
) -> list[ClimateObservationOut]:
    """Return the most recent observation per dataset for Hyderabad."""
    observations = await climate_service.get_latest_by_dataset(
        db, bbox=HYDERABAD_BBOX,
    )
    return [ClimateObservationOut.model_validate(o) for o in observations]
