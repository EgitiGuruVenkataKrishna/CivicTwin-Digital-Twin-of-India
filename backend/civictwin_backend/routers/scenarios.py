"""Scenario management router for CivicTwin.

Provides CRUD for what-if scenarios and a ``/run`` action endpoint that
triggers inference through the decoupled HF Space proxy.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from civictwin_backend.database import get_db
from civictwin_backend.models import ScenarioResult
from civictwin_backend.schemas.scenario import (
    ScenarioCreate,
    ScenarioOut,
    ScenarioResultOut,
)
from civictwin_backend.services import scenario_service
from civictwin_backend.services.inference_client import get_inference_client

router = APIRouter()


# ── Create ──────────────────────────────────────────────────────────────


@router.post("/", response_model=ScenarioOut, status_code=201)
async def create_scenario(
    payload: ScenarioCreate,
    db: AsyncSession = Depends(get_db),
) -> ScenarioOut:
    """Create a new scenario with ``status='pending'``."""
    scenario = await scenario_service.create_scenario(db, payload)
    return ScenarioOut.model_validate(scenario)


# ── List ────────────────────────────────────────────────────────────────


@router.get("/", response_model=list[ScenarioOut])
async def list_scenarios(
    status: str | None = Query(None, description="Filter by status"),
    zone_id: UUID | None = Query(None, description="Filter by zone UUID"),
    db: AsyncSession = Depends(get_db),
) -> list[ScenarioOut]:
    """Return scenarios, optionally filtered by *status* and/or *zone_id*."""
    scenarios = await scenario_service.list_scenarios(db, status=status, zone_id=zone_id)
    return [ScenarioOut.model_validate(s) for s in scenarios]


# ── Get one (with results) ──────────────────────────────────────────────


@router.get("/{scenario_id}", response_model=ScenarioOut)
async def get_scenario(
    scenario_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ScenarioOut:
    """Retrieve a single scenario by UUID (results eagerly loaded)."""
    scenario = await scenario_service.get_scenario(db, scenario_id)
    return ScenarioOut.model_validate(scenario)


# ── Run inference ───────────────────────────────────────────────────────


@router.post("/{scenario_id}/run", response_model=ScenarioResultOut)
async def run_scenario(
    scenario_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ScenarioResultOut:
    """Trigger PINN inference for a scenario via the HF Space proxy.

    Fetches climate data for the scenario's zone, sends it to the
    HF Space ``/predict`` endpoint, stores the result, and updates
    the scenario status to ``completed`` (or ``failed``).
    """
    client = get_inference_client()
    result = await scenario_service.run_scenario(db, scenario_id, client)
    return ScenarioResultOut.model_validate(result)


# ── Results ─────────────────────────────────────────────────────────────


@router.get("/{scenario_id}/results", response_model=list[ScenarioResultOut])
async def get_scenario_results(
    scenario_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> list[ScenarioResultOut]:
    """Return all inference results for a scenario."""
    result = await db.execute(
        select(ScenarioResult)
        .where(ScenarioResult.scenario_id == scenario_id)
        .order_by(ScenarioResult.computed_at.desc())
    )
    results = result.scalars().all()
    return [ScenarioResultOut.model_validate(r) for r in results]
