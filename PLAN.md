# 🗺️ CivicTwin — Development Plan

> **Bharatiya Antariksh Hackathon 2026**
> AI-Powered Climate Digital Twin for Indian Cities — Pilot: Hyderabad

---

## 🏛️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        ZERO-COST HOSTING MAP                            │
├──────────────┬──────────────┬──────────────┬────────────────────────────┤
│   Vercel     │   Render /   │  HF Spaces   │  Supabase                 │
│   (Frontend) │   Railway    │  (ML Infer.)  │  (PostGIS DB)             │
│              │   (FastAPI)  │              │                            │
│  React       │  REST API    │  Dockerized  │  PostgreSQL 15 + PostGIS  │
│  Deck.gl     │  Proxy to HF │  FastAPI +   │  500 MB free tier         │
│  MapLibre    │  PostGIS I/O │  PyTorch     │  Row-Level Security       │
│              │              │  PINN model  │                            │
└──────┬───────┴──────┬───────┴──────┬───────┴────────────┬───────────────┘
       │              │              │                    │
       │   REST/WS    │  httpx proxy │   SQL/PostGIS      │
       └──────────────┘──────────────┘────────────────────┘

Data Sources (free):
  • Google Earth Engine (research quota)
  • MOSDAC (INSAT-3D/3DR — free registration)
  • IMD AWS API (public endpoints)
  • CPCB AQ (public data / OpenAQ mirror)
```

---

## 📁 Project Structure

```
civictwin/
├── .cursorrules                    # Agent rules: enforce decoupled arch
├── .github/
│   └── workflows/
│       ├── lint.yml                # Ruff + ESLint CI
│       ├── test.yml                # pytest + vitest CI
│       └── deploy.yml              # Vercel preview + HF Space push
│
├── backend/                        # FastAPI REST API (Render/Railway)
│   ├── pyproject.toml
│   ├── requirements.txt            # pip-installable deps (no Poetry lock needed)
│   ├── Dockerfile                  # For Render/Railway deployment
│   └── civictwin_backend/
│       ├── __init__.py
│       ├── main.py                 # FastAPI app factory + CORS + lifespan
│       ├── config.py               # Pydantic Settings (env-driven)
│       ├── database.py             # SQLAlchemy async engine + session
│       ├── models/                 # SQLAlchemy ORM (PostGIS geometry)
│       │   ├── __init__.py
│       │   ├── climate.py          # ClimateObservation, ClimateGrid
│       │   ├── zone.py             # PlanningZone
│       │   └── scenario.py         # Scenario, ScenarioResult
│       ├── schemas/                # Pydantic v2 request/response DTOs
│       │   ├── __init__.py
│       │   ├── climate.py
│       │   ├── zone.py
│       │   └── scenario.py
│       ├── routers/                # API route handlers
│       │   ├── __init__.py
│       │   ├── climate.py          # /api/v1/climate/*
│       │   ├── zones.py            # /api/v1/zones/*
│       │   ├── scenarios.py        # /api/v1/scenarios/*
│       │   └── inference.py        # /api/v1/inference/* (HF proxy)
│       ├── services/               # Business logic layer
│       │   ├── __init__.py
│       │   ├── climate_service.py  # PostGIS spatial queries
│       │   ├── inference_client.py # httpx → HF Spaces (decoupled!)
│       │   └── scenario_service.py # Scenario CRUD + result orchestration
│       └── utils/
│           ├── __init__.py
│           └── geo.py              # GeoJSON/bbox helpers
│
├── ml/                             # PINN training + HF Space serving
│   ├── pyproject.toml
│   ├── civictwin_ml/
│   │   ├── __init__.py
│   │   ├── train.py                # Training entrypoint
│   │   ├── pinn.py                 # PINN architecture (PyTorch)
│   │   ├── losses.py               # PDE residual losses
│   │   ├── data_loader.py          # Load from PostGIS exports / .nc files
│   │   └── evaluate.py             # RMSE/MAE at station locations
│   └── hf_space/                   # Dockerized HF Space for inference
│       ├── Dockerfile
│       ├── requirements.txt
│       ├── app.py                  # FastAPI inference server
│       └── model/                  # TorchScript exported model
│
├── etl/                            # Data ingestion pipeline
│   ├── __init__.py
│   ├── ingest.py                   # CLI entrypoint (exists)
│   ├── gee_fetcher.py              # Google Earth Engine client
│   ├── mosdac_fetcher.py           # INSAT-3D/3DR downloader
│   ├── imd_fetcher.py              # IMD AWS station client
│   ├── cpcb_fetcher.py             # CPCB air quality client
│   ├── grid_fuser.py               # Spatial fusion → unified 250m grid
│   └── db_writer.py                # Batch insert to PostGIS
│
├── frontend/                       # React + Deck.gl (Vercel)
│   ├── package.json
│   ├── vite.config.ts
│   ├── vercel.json                 # Vercel config: rewrites to backend
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── index.css               # Design tokens + global styles
│       ├── components/
│       │   ├── MapView.tsx          # Deck.gl + MapLibre GL viewport
│       │   ├── HeatmapLayer.tsx     # ColumnLayer / HeatmapLayer
│       │   ├── ZonePanel.tsx        # Zone selector sidebar
│       │   ├── ScenarioBuilder.tsx  # What-if scenario form
│       │   ├── TimeSlider.tsx       # Temporal navigation
│       │   └── MetricCards.tsx      # KPI cards (temp, AQI, etc.)
│       ├── hooks/
│       │   ├── useClimateData.ts    # SWR/React-Query for climate API
│       │   └── useSimulation.ts     # WebSocket hook for live sim
│       ├── store/
│       │   └── appStore.ts          # Zustand global state
│       ├── services/
│       │   └── api.ts              # Axios instance + endpoints
│       └── types/
│           └── index.ts            # Shared TypeScript interfaces
│
├── infra/
│   ├── .env.example
│   ├── docker-compose.yml          # Local PostGIS + Redis
│   └── supabase/
│       └── migrations/
│           └── 001_init.sql        # PostGIS extension + tables DDL
│
└── README.md
```

---

## 🚦 Phase 1 — Project Setup & Infrastructure (Days 1–3)

### Goals
- Reproducible local dev environment
- PostGIS schema with spatial indices
- CI/CD pipeline (lint → test → deploy)
- All env vars documented and secrets templated

### Tasks

| # | Task | Deliverable |
|---|------|-------------|
| 1.1 | Create `.cursorrules` enforcing decoupled architecture | `.cursorrules` |
| 1.2 | Expand FastAPI skeleton: config, database, routers, models, schemas, services | `backend/civictwin_backend/**` |
| 1.3 | Generate `requirements.txt` from pyproject.toml | `backend/requirements.txt` |
| 1.4 | Write PostGIS migration: enable PostGIS, create tables with geometry columns | `infra/supabase/migrations/001_init.sql` |
| 1.5 | Docker Compose: verify PostGIS + Redis spin up cleanly | `infra/docker-compose.yml` |
| 1.6 | GitHub Actions: add `test.yml` (pytest backend) + `deploy.yml` (preview) | `.github/workflows/` |
| 1.7 | Supabase project creation + connection string in `.env` | Manual + docs |

### Acceptance Criteria
- `docker compose up -d` → PostGIS reachable on `:5432`
- `uvicorn civictwin_backend.main:app --reload` → `/api/v1/health` returns `{"api":"ok","database":"connected"}`
- `ruff check backend/` → 0 errors
- All CI jobs pass on push

---

## 🚦 Phase 2 — Data Pipeline (Days 4–8)

### Goals
- Automated ingestion from GEE, MOSDAC, IMD, CPCB
- Spatial fusion into a unified 250 m × 250 m grid
- Data served from PostGIS with spatial queries

### Tasks

| # | Task | Deliverable |
|---|------|-------------|
| 2.1 | Implement `gee_fetcher.py`: authenticate, query MODIS/Landsat/ERA5, download GeoTIFF | `etl/gee_fetcher.py` |
| 2.2 | Implement `mosdac_fetcher.py`: download INSAT-3D TIR HDF5 files | `etl/mosdac_fetcher.py` |
| 2.3 | Implement `imd_fetcher.py` + `cpcb_fetcher.py`: station data to DataFrame | `etl/imd_fetcher.py`, `etl/cpcb_fetcher.py` |
| 2.4 | Implement `grid_fuser.py`: resample all sources to 250 m grid via rioxarray | `etl/grid_fuser.py` |
| 2.5 | Implement `db_writer.py`: batch upsert fused grid cells to PostGIS | `etl/db_writer.py` |
| 2.6 | Wire up `ingest.py` CLI to call real fetchers | `etl/ingest.py` |
| 2.7 | Backfill 90 days of data for Hyderabad | PostGIS rows |

### Acceptance Criteria
- `python -m etl.ingest --dataset modis_lst --date 2026-06-01` → rows in `climate_observations`
- Spatial query `ST_Within(geom, hyderabad_bbox)` returns expected grid cells
- Data available for at least 3 modalities (LST, AQ, meteorological)

---

## 🚦 Phase 3 — AI / PINN Modeling (Days 6–12)

> [!NOTE]
> Overlaps with Phase 2 — start training as soon as ≥30 days of fused data exist.

### Goals
- Baseline MLP → Physics-Informed Neural Network
- Uncertainty quantification via MC-Dropout or Deep Ensemble
- Exported TorchScript model for serving on HF Spaces

### Tasks

| # | Task | Deliverable |
|---|------|-------------|
| 3.1 | `data_loader.py`: load fused data from PostGIS exports / NetCDF | `ml/civictwin_ml/data_loader.py` |
| 3.2 | Baseline MLP: 4-layer network, MSE loss on LST | `ml/civictwin_ml/pinn.py` (v1) |
| 3.3 | Fourier Feature Embedding for spatial/temporal inputs | `ml/civictwin_ml/pinn.py` (v2) |
| 3.4 | PDE residual losses: heat diffusion + energy balance + advection-diffusion | `ml/civictwin_ml/losses.py` |
| 3.5 | Composite loss with GradNorm adaptive weighting | `ml/civictwin_ml/losses.py` |
| 3.6 | MC-Dropout for uncertainty quantification (hackathon MVP) | `ml/civictwin_ml/pinn.py` |
| 3.7 | `evaluate.py`: RMSE / MAE at IMD station locations | `ml/civictwin_ml/evaluate.py` |
| 3.8 | Export trained model to TorchScript | `ml/civictwin_ml/train.py` |
| 3.9 | Create HF Space: Dockerized FastAPI serving TorchScript model | `ml/hf_space/` |

### Acceptance Criteria
- PINN RMSE < baseline MLP RMSE by ≥15% on held-out stations
- `ml/hf_space/` deployable to HF Spaces with `POST /predict` endpoint
- Inference latency < 2 s for 100 × 100 grid prediction

---

## 🚦 Phase 4 — API & Backend (Days 9–14)

### Goals
- Full REST API serving climate data, zones, and scenarios
- Backend proxies inference to HF Space (decoupled architecture)
- WebSocket for live simulation streaming

### Tasks

| # | Task | Deliverable |
|---|------|-------------|
| 4.1 | `climate.py` router: `/snapshot`, `/timeseries`, spatial queries via PostGIS | `backend/.../routers/climate.py` |
| 4.2 | `zones.py` router: CRUD for planning zones (GeoJSON polygons) | `backend/.../routers/zones.py` |
| 4.3 | `scenarios.py` router: create scenario → trigger inference → store results | `backend/.../routers/scenarios.py` |
| 4.4 | `inference.py` router + `inference_client.py`: httpx proxy to HF Space | `backend/.../routers/inference.py` |
| 4.5 | WebSocket endpoint `/ws/simulation` for live result streaming | `backend/.../main.py` |
| 4.6 | Redis caching layer for hot climate data | `backend/.../services/` |
| 4.7 | `Dockerfile` for backend (Render/Railway deployment) | `backend/Dockerfile` |
| 4.8 | Integration tests: pytest-asyncio + httpx.AsyncClient | `backend/tests/` |

### Acceptance Criteria
- All API endpoints return correct GeoJSON/JSON
- `POST /api/v1/scenarios` triggers HF Space inference and returns results within 5 s
- WebSocket streams simulation frames to connected client
- `pytest backend/` → all green

---

## 🚦 Phase 5 — Frontend Dashboard (Days 12–18)

### Goals
- Production-quality 3D climate visualization
- Interactive what-if scenario builder
- Deployed on Vercel, connected to live backend

### Tasks

| # | Task | Deliverable |
|---|------|-------------|
| 5.1 | `MapView.tsx`: Deck.gl + MapLibre GL JS, initial viewport on Hyderabad | `frontend/src/components/MapView.tsx` |
| 5.2 | `HeatmapLayer.tsx`: ColumnLayer for LST, ScatterplotLayer for stations | `frontend/src/components/HeatmapLayer.tsx` |
| 5.3 | `ZonePanel.tsx`: clickable zone selector, zone stats | `frontend/src/components/ZonePanel.tsx` |
| 5.4 | `ScenarioBuilder.tsx`: form to create what-if scenarios | `frontend/src/components/ScenarioBuilder.tsx` |
| 5.5 | `TimeSlider.tsx`: temporal navigation with playback | `frontend/src/components/TimeSlider.tsx` |
| 5.6 | `MetricCards.tsx`: KPI cards (avg temp, AQI, confidence) | `frontend/src/components/MetricCards.tsx` |
| 5.7 | Zustand store + API service layer | `frontend/src/store/`, `frontend/src/services/` |
| 5.8 | `vercel.json`: API rewrites to backend URL | `frontend/vercel.json` |
| 5.9 | Dark theme polish, micro-animations, responsive layout | CSS + components |
| 5.10 | Deploy to Vercel + connect custom domain | Vercel dashboard |

### Acceptance Criteria
- Dashboard loads in < 3 s on 4G connection
- Heatmap renders ≥10,000 grid cells at 60 fps
- Scenario simulation round-trip (create → infer → visualize) < 10 s
- Lighthouse Performance score ≥ 80

---

## 🔑 Free-Tier Service Limits (Monitor These)

| Service | Free Tier | Limit to Watch |
|---------|-----------|----------------|
| **Supabase** | 500 MB DB, 1 GB bandwidth, 50K MAU | DB size with PostGIS data |
| **Vercel** | 100 GB bandwidth, 12 serverless fn regions | No serverless fns (static + rewrites only) |
| **HF Spaces** | 2 vCPU, 16 GB RAM (CPU), ZeroGPU queue | Inference latency on CPU |
| **Render** | 750 hrs/mo (spin down on idle) | Cold start time (~30 s) |
| **Google Earth Engine** | Research/Education quota | API call rate limits |
| **GitHub Actions** | 2000 min/mo (public repos) | CI runtime |

---

## 📊 Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| HF Space cold start too slow | Bad UX on first scenario | Pre-warm with cron ping; show loading animation |
| Supabase 500 MB limit hit | Cannot store more data | Aggregate older data; use 500 m grid for archive |
| MOSDAC API unreliable | Missing INSAT data | Fall back to ERA5 reanalysis from GEE |
| PINN training too slow on CPU | Can't iterate on model | Use Google Colab (free GPU) for training |
| Render cold start (30 s) | API timeout on first call | Health-check cron; frontend retry with skeleton UI |
