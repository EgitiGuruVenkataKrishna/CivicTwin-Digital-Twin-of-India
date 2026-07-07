"""Climate data service for CivicTwin.

Provides async functions that query PostGIS-backed climate observations
using SQLAlchemy + GeoAlchemy2 spatial functions.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from geoalchemy2.functions import ST_DWithin, ST_Within
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from civictwin_backend.models import ClimateObservation
from civictwin_backend.utils.geo import HYDERABAD_BBOX


async def get_snapshot(
    db: AsyncSession,
    bbox: dict[str, float],
    dataset: str | None = None,
    limit: int = 1000,
) -> list[Any]:
    """Return climate observations whose geometry falls within *bbox*.

    Uses ``ST_MakeEnvelope`` + ``ST_Within`` to build the PostGIS
    spatial filter.
    """
    envelope = func.ST_MakeEnvelope(
        bbox["west"],
        bbox["south"],
        bbox["east"],
        bbox["north"],
        4326,  # SRID WGS-84
    )

    stmt = (
        select(ClimateObservation)
        .where(ST_Within(ClimateObservation.geometry, envelope))
    )

    if dataset:
        stmt = stmt.where(ClimateObservation.dataset == dataset)

    stmt = stmt.order_by(ClimateObservation.observed_at.desc()).limit(limit)

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_timeseries(
    db: AsyncSession,
    lat: float,
    lon: float,
    dataset: str,
    start_date: date,
    end_date: date,
) -> list[Any]:
    """Return a time-ordered series of observations near (*lat*, *lon*).

    ``ST_DWithin`` is used with a 0.005-degree buffer (~500 m at the
    latitude of Hyderabad) to find the nearest observation point.
    """
    point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)

    stmt = (
        select(ClimateObservation)
        .where(
            ST_DWithin(ClimateObservation.geometry, point, 0.005),
            ClimateObservation.dataset == dataset,
            ClimateObservation.observed_at >= datetime.combine(start_date, datetime.min.time()),
            ClimateObservation.observed_at <= datetime.combine(end_date, datetime.max.time()),
        )
        .order_by(ClimateObservation.observed_at.asc())
    )

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_latest_by_dataset(
    db: AsyncSession,
    bbox: dict[str, float] | None = None,
) -> list[Any]:
    """Return the most recent observation per dataset.

    Uses ``DISTINCT ON (dataset)`` ordered by ``observed_at DESC``.
    If *bbox* is provided, restricts to observations within it;
    otherwise defaults to the Hyderabad pilot-city bbox.
    """
    if bbox is None:
        bbox = HYDERABAD_BBOX

    envelope = func.ST_MakeEnvelope(
        bbox["west"],
        bbox["south"],
        bbox["east"],
        bbox["north"],
        4326,
    )

    stmt = (
        select(ClimateObservation)
        .where(ST_Within(ClimateObservation.geometry, envelope))
        .distinct(ClimateObservation.dataset)
        .order_by(ClimateObservation.dataset, ClimateObservation.observed_at.desc())
    )

    result = await db.execute(stmt)
    return list(result.scalars().all())
