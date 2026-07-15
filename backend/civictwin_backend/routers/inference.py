"""Direct inference proxy router for CivicTwin.

Exposes lightweight endpoints that let the frontend call the HF-Space
PINN model directly for quick predictions without creating a full
scenario record.  Also provides health and model-info probes.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from civictwin_backend.schemas.scenario import InferenceRequest, InferenceResponse
from civictwin_backend.services.inference_client import get_inference_client

router = APIRouter()


# ── Direct prediction ───────────────────────────────────────────────────


@router.post("/predict", response_model=InferenceResponse)
async def predict(payload: InferenceRequest) -> InferenceResponse:
    """Forward an inference request to the HF Space and return predictions.

    This is a thin proxy — the backend never imports ``torch``.
    """
    client = get_inference_client()
    return await client.predict(
        grid_data=payload.grid_data,
        scenario_params=payload.scenario_params,
        model_version=payload.model_version,
    )


# ── Health check ────────────────────────────────────────────────────────


@router.get("/health")
async def health_check() -> dict:
    """Ping the HF Space to verify it is reachable."""
    client = get_inference_client()
    is_healthy = await client.health_check()
    return {
        "hf_space_healthy": is_healthy,
        "status": "ok" if is_healthy else "degraded",
    }


# ── Model metadata ─────────────────────────────────────────────────────


@router.get("/model-info")
async def model_info() -> dict:
    """Return model metadata from the HF Space."""
    client = get_inference_client()
    try:
        info = await client.get_model_info()
        return info
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to retrieve model info: {exc}",
        )
