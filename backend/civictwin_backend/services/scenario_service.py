"""Scenario service for CivicTwin.

CRUD operations and inference orchestration for what-if scenarios.
When a scenario is *run*, this service:

1. Loads the scenario and its related zone from the DB.
2. Fetches current climate data for the zone's bounding box.
3. Forwards the grid + intervention parameters to the HF Space via
   ``InferenceClient``.
4. Stores the result as a ``ScenarioResult`` row.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from civictwin_backend.models import Scenario, ScenarioResult, Zone
from civictwin_backend.schemas.scenario import ScenarioCreate
from civictwin_backend.services.climate_service import get_snapshot
from civictwin_backend.services.inference_client import InferenceClient

logger = logging.getLogger(__name__)


# ── CRUD ────────────────────────────────────────────────────────────────


async def create_scenario(
    db: AsyncSession,
    scenario_data: ScenarioCreate,
) -> Scenario:
    """Insert a new scenario with ``status='pending'``."""
    scenario = Scenario(
        name=scenario_data.name,
        description=scenario_data.description,
        zone_id=scenario_data.zone_id,
        intervention_type=scenario_data.intervention_type,
        parameters=scenario_data.parameters,
        status="pending",
    )
    db.add(scenario)
    await db.commit()
    await db.refresh(scenario)
    return scenario


async def list_scenarios(
    db: AsyncSession,
    status: str | None = None,
    zone_id: UUID | None = None,
) -> Sequence[Scenario]:
    """Return scenarios, optionally filtered by *status* and/or *zone_id*."""
    stmt = select(Scenario)
    if status:
        stmt = stmt.where(Scenario.status == status)
    if zone_id:
        stmt = stmt.where(Scenario.zone_id == zone_id)
    stmt = stmt.order_by(Scenario.created_at.desc())

    result = await db.execute(stmt)
    return result.scalars().all()


async def get_scenario(
    db: AsyncSession,
    scenario_id: UUID,
) -> Scenario:
    """Load a single scenario with its results eagerly loaded."""
    stmt = (
        select(Scenario)
        .where(Scenario.id == scenario_id)
        .options(selectinload(Scenario.results))
    )
    result = await db.execute(stmt)
    scenario = result.scalar_one_or_none()
    if scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario


# ── Run inference ───────────────────────────────────────────────────────


async def run_scenario(
    db: AsyncSession,
    scenario_id: UUID,
    inference_client: InferenceClient,
) -> ScenarioResult:
    """Execute inference for a scenario and persist the result.

    Steps
    -----
    1. Validate scenario exists and is runnable.
    2. Load the related zone to determine its spatial extent.
    3. Fetch the latest climate snapshot for the zone's bbox.
    4. Call ``inference_client.predict()`` with the grid + parameters.
    5. Store a ``ScenarioResult`` row and flip ``status`` to
       ``'completed'`` (or ``'failed'`` on error).
    """
    scenario = await get_scenario(db, scenario_id)

    # Load related zone for spatial context
    zone_result = await db.execute(
        select(Zone).where(Zone.id == scenario.zone_id)
    )
    zone = zone_result.scalar_one_or_none()
    if zone is None:
        raise HTTPException(status_code=404, detail="Related zone not found")

    # Build a bbox from the zone's geojson for the climate query
    coords = zone.geojson.get("coordinates", [[]])[0]
    if not coords:
        raise HTTPException(status_code=400, detail="Zone has no coordinates")

    lons = [c[0] for c in coords]
    lats = [c[1] for c in coords]
    zone_bbox = {
        "west": min(lons),
        "south": min(lats),
        "east": max(lons),
        "north": max(lats),
    }

    try:
        # Fetch climate data for the zone
        observations = await get_snapshot(db, zone_bbox, dataset=None, limit=500)

        grid_data = [
            {
                "lat": obs.lat,
                "lon": obs.lon,
                "properties": obs.properties,
            }
            for obs in observations
        ]

        # Call HF Space
        inference_response = await inference_client.predict(
            grid_data=grid_data,
            scenario_params=scenario.parameters,
            model_version="latest",
        )

        # Compute summary metrics
        predictions = inference_response.predictions
        temps = [p.get("predicted_temp", 0) for p in predictions if "predicted_temp" in p]
        aqis = [p.get("predicted_aqi", 0) for p in predictions if "predicted_aqi" in p]

        metrics: dict[str, Any] = {
            "prediction_count": len(predictions),
            "inference_time_ms": inference_response.inference_time_ms,
        }
        if temps:
            metrics["avg_predicted_temp"] = sum(temps) / len(temps)
            metrics["max_predicted_temp"] = max(temps)
            metrics["min_predicted_temp"] = min(temps)
        if aqis:
            metrics["avg_predicted_aqi"] = sum(aqis) / len(aqis)

        # Persist result
        scenario_result = ScenarioResult(
            scenario_id=scenario_id,
            result_grid={"predictions": predictions},
            uncertainty={"model_version": inference_response.model_version},
            metrics=metrics,
            computed_at=datetime.now(UTC),
            model_version=inference_response.model_version,
        )
        db.add(scenario_result)

        scenario.status = "completed"
        scenario.updated_at = datetime.now(UTC)
        await db.commit()
        await db.refresh(scenario_result)

        return scenario_result

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Scenario %s inference failed", scenario_id)
        scenario.status = "failed"
        scenario.updated_at = datetime.now(UTC)
        await db.commit()
        raise HTTPException(
            status_code=500,
            detail=f"Inference failed: {exc}",
        )
