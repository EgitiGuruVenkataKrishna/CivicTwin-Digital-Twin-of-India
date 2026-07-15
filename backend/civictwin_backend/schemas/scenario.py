"""Scenario & inference schemas for CivicTwin.

Defines Pydantic v2 models for what-if scenarios (e.g. add green space,
change albedo) and the inference request/response contract used to
communicate with the HF-Space-hosted PINN model.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

INTERVENTION_TYPES = Literal[
    "add_green_space",
    "add_industrial",
    "add_water_body",
    "change_albedo",
    "add_ventilation_corridor",
]


# ── Scenario CRUD ───────────────────────────────────────────────────────


class ScenarioCreate(BaseModel):
    """Payload for creating a new what-if scenario."""

    name: str
    description: str | None = None
    zone_id: UUID
    intervention_type: INTERVENTION_TYPES
    parameters: dict  # e.g. {"area_fraction": 0.3, "albedo_delta": -0.1}


class ScenarioOut(BaseModel):
    """Scenario representation returned to the client."""

    id: UUID
    name: str
    description: str | None = None
    zone_id: UUID
    intervention_type: str
    parameters: dict
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ScenarioResultOut(BaseModel):
    """Result of a scenario inference run."""

    id: UUID
    scenario_id: UUID
    result_grid: dict
    uncertainty: dict
    metrics: dict
    computed_at: datetime | None = None
    model_version: str | None = None

    model_config = ConfigDict(from_attributes=True)


# ── Inference contract (HF Space proxy) ─────────────────────────────────


class InferenceRequest(BaseModel):
    """Payload sent to the HF Space /predict endpoint."""

    grid_data: list[dict]  # input grid cells with lat, lon, features
    scenario_params: dict
    model_version: str = "latest"


class InferenceResponse(BaseModel):
    """Response received from the HF Space /predict endpoint."""

    predictions: list[dict]  # lat, lon, predicted_temp, predicted_aqi, confidence
    model_version: str
    inference_time_ms: float
