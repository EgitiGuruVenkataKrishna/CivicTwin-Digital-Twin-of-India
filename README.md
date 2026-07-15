# 🛰️ CivicTwin — AI-Powered Climate Digital Twin of India

> **A high-fidelity, dynamic virtual replica of India's regional climate system built for Bharatiya Antariksh Hackathon 2026 (Problem Statement 5). Ingests space observations and meteorological networks, applies physics-informed solvers, and delivers interactive multi-sector "what-if" simulations for climate adaptation.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](backend)
[![React: 18.2](https://img.shields.io/badge/React-18.2-teal.svg)](frontend)
[![Mapbox/MapLibre](https://img.shields.io/badge/Geospatial-Deck.gl%20%7C%20MapLibre-emerald.svg)](frontend)

---

## 🎯 The Challenge: ISRO Problem Statement 5

### **Problem Context**
India's regional climate monitoring is fragmented across incompatible databases and file formats. Traditional weather models operate on historical data, providing static, descriptive snapshots without the interactive "what-if" projection tools required by climate adaptation planners.

### **Our Solution**
**CivicTwin** creates a dynamic virtual replica of India's climate system over selected pilot catchments. It integrates multi-source space and ground-station products, runs a **Physics-Informed Neural Network (PINN)** solver, and visualizes immediate projections for agricultural yield, reservoir water levels, and drought indices.

```
┌──────────────────────────────────────────────────────────────┐
│                  INPUTS (INSAT, IMD, GEE)                     │
└──────────────┬────────────────────────────────┬──────────────┘
               │                                │
        [Evaporation]                      [Precipitation]
               │                                │
               ▼                                ▼
┌──────────────────────────────────────────────────────────────┐
│        PHYSICS-INFORMED SOLVER (PENMAN-MONTEITH)             │
└──────────────┬────────────────────────────────┬──────────────┘
               │                                │
               ▼                                ▼
┌──────────────────────────────────────────────────────────────┐
│       DECISION SECTORS (Crop Yield, SPEI, Reservoirs)        │
└──────────────────────────────────────────────────────────────┘
```

---

## 💡 Core Pillars & Innovations

### 1. Heterogeneous Data Fusion Pipeline
Ingests and aligns diverse Earth Observation and ground networks:
*   **INSAT Land Surface Temperature (LST)**: `3RIMG_L2B_LST` via MOSDAC.
*   **INSAT Multi-sensor Precipitation**: `3RIMG_L2B_IMC` via MOSDAC.
*   **IMD Gridded Baseline Daily Precipitation**: $0.25^\circ \times 0.25^\circ$ grid arrays.
*   **IMD Gridded Baseline Temperatures**: $1.0^\circ \times 1.0^\circ$ grid arrays.
*   **Landsat-8 Thermal Infrared Sensor (TIRS)**: High-resolution LST anomalies via Google Earth Engine (GEE).
*   **CPCB Air Quality Networks**: Live spatial particulate markers.

### 2. Physics-Informed Numerical Engine
Instead of generic black-box regressions, the simulation core is guided by physical conservation laws:
*   **Penman-Monteith Formulation**: Calculates regional evapotranspiration ($ET_0$) as a function of temperature anomalies ($\Delta T$), solar radiation, and wind parameters, predicting soil dehydration:
    $$ET_0 \propto \frac{\Delta (R_n - G) + \rho_a c_p \frac{(e_s - e_a)}{r_a}}{\Delta + \gamma \left(1 + \frac{r_s}{r_a}\right)}$$
*   **SPEI (Standardized Precipitation-Evapotranspiration Index)**: Evaluates drought severity classifications (*Normal*, *Moderate*, *Severe*, *Extreme*) by calculating cumulative water balance deficits.
*   **Hydrological Runoff Modeling**: Simulates reservoir inflows as a function of monsoon precipitation deviations and evaporation losses.

### 3. Interactive 3D Digital Twin Interface
A React dashboard using Deck.gl and MapLibre GL for rendering:
*   **Interactive Tooltips**: Hovering over planning zones (e.g. Hussain Sagar, HITEC City) or weather stations shows exact coordinates and data values.
*   **Variable Layer Modes**: Toggling focus between *Agriculture & Crop Health*, *Water Security & Reservoirs*, and *Disaster Risk & Wet-Bulb Heat Stress* shifts the map's visual representation instantly.
*   **Live Simulation Progress**: Progress calculations stream in real-time over WebSockets, animating the 3D map as the physics solver converges.

---

## 🏗️ System Architecture

```
                       ┌──────────────────────┐
                       │   ISRO Earth Obs.    │
                       │   (MOSDAC / Bhuvan)  │
                       └──────────┬───────────┘
                                  │
                                  ▼
┌──────────────────┐   ┌──────────────────────┐   ┌──────────────────┐
│  IMD Gridded     │──▸│   ETL Ingestion &    │◂──│  GEE Landsat /   │
│  Rain/Temp Bins  │   │   Fuser (Python)     │   │  CPCB Stations   │
└──────────────────┘   └──────────┬───────────┘   └──────────────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │   Supabase DB        │
                       │   (Postgres/PostGIS) │
                       └──────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │   FastAPI Backend    │
                       │   (Uvicorn Middleware)│
                       └──────────┬───────────┘
                                 / \
                                /   \
                               /     \
    WebSocket Progress Streams/       \HTTP REST API
                             ▼         ▼
                       ┌──────────────────────┐
                       │    React Dashboard   │
                       │    (Deck.gl Map)     │
                       └──────────────────────┘
```

---

## 📁 Repository Directory Structure

```
civictwin/
├── backend/          # FastAPI server, SQL database migrations, routing & WS
│   ├── civictwin_backend/
│   │   ├── models/   # PostGIS Database Models (PlanningZone, ClimateObservation)
│   │   ├── routers/  # WS Streaming, Scenarios Run, and Climate Endpoints
│   │   └── services/ # DB querying, geometry bounds extraction, GEE adapters
│   └── requirements.txt
├── frontend/         # React + Vite + TypeScript web application
│   ├── src/
│   │   ├── components/ # MapComponent (Deck.gl/MapLibre), Sidebar, Metrics, InfoModal
│   │   ├── services/   # WebSocket Manager & API client
│   │   └── store/      # Zustand app state (Climate parameters & metrics)
│   └── package.json
├── etl/              # Ingestion and alignment scripts for IMD/INSAT grids
├── ml/               # PyTorch PINN model physics training code
├── infra/            # Docker configurations (local database testbeds)
└── README.md
```

---

## 🚀 Quick Start & Installation

### 1. Pre-requisites
*   Python 3.11+
*   Node.js 18+
*   PostgreSQL / Supabase instance (with PostGIS enabled)

Create a `.env` file in the `backend/` directory (you can copy `.env.example` from `infra/` or create it manually):
```env
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/postgres
SUPABASE_URL=https://<your-project-id>.supabase.co
SUPABASE_ANON_KEY=<your-anon-key>
REDIS_URL=redis://localhost:6379/0
GEE_SERVICE_ACCOUNT_EMAIL=<your-service-account-email>
HF_TOKEN=hf_<your-huggingface-token>
HF_SPACE_URL=https://<your-space-name>.hf.space
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

### 3. Launch the Backend Server
```bash
cd backend
pip install -r requirements.txt
uvicorn civictwin_backend.main:app --port 8000 --host 127.0.0.1
```
*Note: The API automatically launches, verifies the DB connection, and seeds pilot coordinate geometries for Hyderabad.*

### 4. Launch the Frontend Dashboard
```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1
```
Open [http://127.0.0.1:5173/](http://127.0.0.1:5173/) in your web browser.

---

## 👥 The CivicTwin Team
*   **Guru Venkata Krishna Egiti** (Team Leader) — VIT-AP University
*   **Prasad Mediboina** (Member) — MVJ College of Engineering
*   **Shree Harsha R** (Member) — VIT-AP University
*   **Sunayana Padhy** (Member) — VIT-AP University

---

## 📜 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
