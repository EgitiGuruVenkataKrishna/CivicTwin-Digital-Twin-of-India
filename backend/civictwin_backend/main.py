"""CivicTwin Backend — FastAPI entrypoint.

Bharatiya Antariksh Hackathon 2026 | Team CivicTwin
AI-powered Climate Digital Twin for Indian Cities — Pilot: Hyderabad

Architecture: DECOUPLED
  • Backend  → Render  (FastAPI + asyncpg)
  • Frontend → Vercel  (React / Deck.gl)
  • ML       → HF Spaces (PyTorch PINN)
  • DB       → Supabase PostGIS

Run locally with:
    uvicorn civictwin_backend.main:app --reload --port 8000
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Any

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from civictwin_backend.config import settings
from civictwin_backend.database import async_session, init_db
from civictwin_backend.routers import (
    climate_router,
    inference_router,
    scenarios_router,
    simulation_router,
    zones_router,
)

logger = logging.getLogger(__name__)


# ── Lifespan ─────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    """Async lifespan: startup / shutdown hooks."""
    # ── Startup ──────────────────────────────────────────────────────────
    logging.basicConfig(level=settings.LOG_LEVEL)
    logger.info(
        "🚀  CivicTwin API starting  |  %s v%s  |  pilot=%s",
        settings.PROJECT_NAME,
        settings.VERSION,
        settings.PILOT_CITY,
    )
    logger.info("   DB  → %s", settings.DATABASE_URL[:40] + "…")
    logger.info("   HF  → %s", settings.HF_SPACE_URL)
    logger.info("   CORS → %s", settings.CORS_ORIGINS)

    # Create tables in dev mode (production uses Alembic migrations).
    try:
        await init_db()
        logger.info("   DB tables ensured (dev mode).")
    except Exception as exc:
        logger.warning("   ⚠  Could not init DB: %s", exc)

    yield

    # ── Shutdown ─────────────────────────────────────────────────────────
    logger.info("🛑  CivicTwin API shutting down.")


# ── Application factory ─────────────────────────────────────────────────
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-powered Climate Digital Twin for Indian Cities",
    version=settings.VERSION,
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Mount routers ────────────────────────────────────────────────────────
app.include_router(climate_router, prefix="/api/v1/climate", tags=["Climate"])
app.include_router(zones_router, prefix="/api/v1/zones", tags=["Zones"])
app.include_router(scenarios_router, prefix="/api/v1/scenarios", tags=["Scenarios"])
app.include_router(inference_router, prefix="/api/v1/inference", tags=["Inference"])
app.include_router(simulation_router, prefix="/api/v1/simulation", tags=["Simulation"])


# ── Root & health ────────────────────────────────────────────────────────
@app.get("/")
async def root():
    """Health check / landing."""
    return {
        "service": "civictwin-api",
        "version": settings.VERSION,
        "status": "ok",
        "pilot_city": settings.PILOT_CITY,
        "team": "Bharatiya Antariksh Hackathon 2026 | Team CivicTwin",
    }


@app.get("/api/v1/health")
async def health():
    """Detailed health check — probes database and HF Space inference."""
    result: dict[str, Any] = {
        "api": "ok",
        "database": "unknown",
        "inference": "unknown",
    }

    # ── Database probe ───────────────────────────────────────────────────
    try:
        async with async_session() as session:
            await session.execute(text("SELECT 1"))
        result["database"] = "ok"
    except Exception as exc:
        result["database"] = f"error: {exc}"

    # ── HF Space inference probe ─────────────────────────────────────────
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{settings.HF_SPACE_URL}/health")
            result["inference"] = "ok" if resp.status_code == 200 else f"http_{resp.status_code}"
    except Exception as exc:
        result["inference"] = f"unreachable: {exc}"

    return result
