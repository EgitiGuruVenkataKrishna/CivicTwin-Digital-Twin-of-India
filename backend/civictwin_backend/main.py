"""CivicTwin Backend — FastAPI entrypoint.

Run with:
    uvicorn civictwin_backend.main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CivicTwin API",
    description="AI-powered Climate Digital Twin for Indian Cities",
    version="0.1.0",
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check / landing."""
    return {
        "service": "civictwin-api",
        "version": "0.1.0",
        "status": "ok",
        "pilot_city": "Hyderabad",
    }


@app.get("/api/v1/health")
async def health():
    """Detailed health check."""
    return {
        "api": "ok",
        "database": "not_connected",  # TODO: check Supabase PostGIS
        "inference": "not_connected",  # TODO: check HF Spaces
    }


# ---------------------------------------------------------------------------
# TODO: Add routers for:
#   /api/v1/tiles/{z}/{x}/{y}        — MVT tiles from PostGIS
#   /api/v1/climate/snapshot          — current climate state for bbox
#   /api/v1/climate/timeseries        — historical time-series for point/zone
#   /api/v1/zones                     — CRUD for planning zones
#   /api/v1/scenarios                 — create what-if scenarios
#   /api/v1/scenarios/{id}/results    — retrieve simulation results
#   /ws/simulation                    — WebSocket for live simulation preview
# ---------------------------------------------------------------------------
