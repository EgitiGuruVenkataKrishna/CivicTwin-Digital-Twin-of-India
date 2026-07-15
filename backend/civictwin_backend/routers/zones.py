"""Zone management router for CivicTwin.

Full CRUD for urban zones (residential, commercial, industrial,
green_space, water_body).  GeoJSON Polygon geometries are converted to
PostGIS-compatible WKB on write.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import mapping, shape
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from civictwin_backend.database import get_db
from civictwin_backend.models import PlanningZone
from civictwin_backend.schemas.zone import ZoneCreate, ZoneOut, ZoneUpdate

router = APIRouter()


def _zone_to_out(zone: PlanningZone) -> ZoneOut:
    """Convert a PlanningZone ORM instance to a ZoneOut schema."""
    geojson = mapping(to_shape(zone.geom)) if zone.geom else {}
    return ZoneOut(
        id=zone.id,
        name=zone.name,
        zone_type=zone.zone_type,
        geojson=geojson,
        area_sqkm=zone.area_sqkm,
        properties=zone.properties,
        created_at=zone.created_at,
        updated_at=zone.updated_at,
    )


# ── Create ──────────────────────────────────────────────────────────────


@router.post("/", response_model=ZoneOut, status_code=201)
async def create_zone(
    payload: ZoneCreate,
    db: AsyncSession = Depends(get_db),
) -> ZoneOut:
    """Create a new zone from a GeoJSON Polygon geometry."""
    # Convert GeoJSON → Shapely → WKB Element
    shapely_geom = shape(payload.geojson)
    wkb_geom = from_shape(shapely_geom, srid=4326)

    zone = PlanningZone(
        name=payload.name,
        zone_type=payload.zone_type,
        geom=wkb_geom,
        properties=payload.properties,
    )
    db.add(zone)
    await db.commit()
    await db.refresh(zone)
    return _zone_to_out(zone)


# ── List ────────────────────────────────────────────────────────────────


@router.get("/", response_model=list[ZoneOut])
async def list_zones(
    zone_type: str | None = Query(None, description="Filter by zone type"),
    db: AsyncSession = Depends(get_db),
) -> list[ZoneOut]:
    """Return all zones, optionally filtered by ``zone_type``."""
    stmt = select(PlanningZone)
    if zone_type:
        stmt = stmt.where(PlanningZone.zone_type == zone_type)
    stmt = stmt.order_by(PlanningZone.created_at.desc())

    result = await db.execute(stmt)
    zones = result.scalars().all()
    return [_zone_to_out(z) for z in zones]


# ── Get one ─────────────────────────────────────────────────────────────


@router.get("/{zone_id}", response_model=ZoneOut)
async def get_zone(
    zone_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ZoneOut:
    """Retrieve a single zone by its UUID."""
    result = await db.execute(select(PlanningZone).where(PlanningZone.id == zone_id))
    zone = result.scalar_one_or_none()
    if zone is None:
        raise HTTPException(status_code=404, detail="Zone not found")
    return _zone_to_out(zone)


# ── Partial update ──────────────────────────────────────────────────────


@router.patch("/{zone_id}", response_model=ZoneOut)
async def update_zone(
    zone_id: UUID,
    payload: ZoneUpdate,
    db: AsyncSession = Depends(get_db),
) -> ZoneOut:
    """Partially update a zone's mutable fields."""
    result = await db.execute(select(PlanningZone).where(PlanningZone.id == zone_id))
    zone = result.scalar_one_or_none()
    if zone is None:
        raise HTTPException(status_code=404, detail="Zone not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(zone, field, value)

    await db.commit()
    await db.refresh(zone)
    return _zone_to_out(zone)


# ── Delete ──────────────────────────────────────────────────────────────


@router.delete("/{zone_id}", status_code=204)
async def delete_zone(
    zone_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a zone by its UUID."""
    result = await db.execute(select(PlanningZone).where(PlanningZone.id == zone_id))
    zone = result.scalar_one_or_none()
    if zone is None:
        raise HTTPException(status_code=404, detail="Zone not found")

    await db.delete(zone)
    await db.commit()
