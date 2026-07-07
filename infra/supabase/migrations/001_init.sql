-- ==========================================================================
-- CivicTwin — Initial PostGIS Migration
-- Bharatiya Antariksh Hackathon 2026 | Pilot City: Hyderabad
-- Supabase PostgreSQL + PostGIS | SRID 4326 (WGS 84)
-- ==========================================================================

-- 1. Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- ==========================================================================
-- 2. climate_observations — raw sensor / satellite readings
-- ==========================================================================
CREATE TABLE climate_observations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataset         VARCHAR(128) NOT NULL,          -- e.g. 'INSAT-3D_TIR1', 'CPCB_AQI'
    observed_at     TIMESTAMPTZ  NOT NULL,
    geom            GEOMETRY(Point, 4326) NOT NULL,
    properties      JSONB        NOT NULL DEFAULT '{}'::jsonb,
                    -- Expected keys: temp_k, aqi, humidity, wind_speed_ms,
                    --                pressure_hpa, precipitation_mm, etc.
    grid_cell_id    VARCHAR(64),                    -- links to climate_grid.cell_id
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT now()
);

COMMENT ON TABLE climate_observations IS
    'Raw climate data points ingested from satellite (INSAT/IMD) and ground-station '
    'sources. Each row is a single observation at a point in space and time. '
    'The properties JSONB stores variable-specific values (temperature, AQI, etc.).';

-- ==========================================================================
-- 3. climate_grid — spatial grid covering Hyderabad (250 m default)
-- ==========================================================================
CREATE TABLE climate_grid (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cell_id         VARCHAR(64) NOT NULL UNIQUE,    -- e.g. 'HYD_250m_R042_C117'
    geom            GEOMETRY(Polygon, 4326) NOT NULL,
    centroid        GEOMETRY(Point, 4326) NOT NULL,
    resolution_m    INT NOT NULL DEFAULT 250,
    metadata        JSONB DEFAULT '{}'::jsonb       -- elevation, land_use, etc.
);

COMMENT ON TABLE climate_grid IS
    'Regular spatial grid (default 250 m) covering the Hyderabad pilot area. '
    'Used to aggregate observations and anchor model predictions to fixed cells.';

-- ==========================================================================
-- 4. planning_zones — urban planning regions
-- ==========================================================================
CREATE TABLE planning_zones (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(256) NOT NULL,
    zone_type       VARCHAR(64)  NOT NULL
                    CHECK (zone_type IN (
                        'residential', 'commercial', 'industrial',
                        'green_space', 'water_body', 'mixed_use',
                        'transportation', 'institutional'
                    )),
    geom            GEOMETRY(Polygon, 4326) NOT NULL,
    area_sqkm       DOUBLE PRECISION,
    properties      JSONB DEFAULT '{}'::jsonb,      -- population_density, tree_cover, etc.
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE planning_zones IS
    'Urban planning polygons representing distinct land-use zones in Hyderabad. '
    'Scenarios are linked to zones to model localised climate interventions.';

-- ==========================================================================
-- 5. scenarios — what-if climate intervention definitions
-- ==========================================================================
CREATE TABLE scenarios (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                VARCHAR(256) NOT NULL,
    description         TEXT,
    zone_id             UUID NOT NULL REFERENCES planning_zones(id) ON DELETE CASCADE,
    intervention_type   VARCHAR(128) NOT NULL,      -- e.g. 'tree_planting', 'cool_roof', 'water_feature'
    parameters          JSONB NOT NULL DEFAULT '{}'::jsonb,
                        -- e.g. { "tree_count": 5000, "species": "neem", "canopy_cover_pct": 35 }
    status              VARCHAR(32) NOT NULL DEFAULT 'pending'
                        CHECK (status IN ('pending', 'running', 'completed', 'failed')),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE scenarios IS
    'User-defined what-if scenarios for climate interventions. Each scenario '
    'targets a specific planning zone and describes the intervention parameters '
    'to be evaluated by the PINN model.';

-- ==========================================================================
-- 6. scenario_results — PINN model output per scenario
-- ==========================================================================
CREATE TABLE scenario_results (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scenario_id     UUID NOT NULL REFERENCES scenarios(id) ON DELETE CASCADE,
    result_grid     JSONB NOT NULL DEFAULT '{}'::jsonb,
                    -- Predicted values per grid cell, e.g.:
                    -- { "HYD_250m_R042_C117": { "delta_temp_k": -1.2, "delta_aqi": -5 } }
    uncertainty     JSONB NOT NULL DEFAULT '{}'::jsonb,
                    -- Confidence intervals, e.g.:
                    -- { "HYD_250m_R042_C117": { "ci_95_lower": -1.5, "ci_95_upper": -0.9 } }
    metrics         JSONB NOT NULL DEFAULT '{}'::jsonb,
                    -- Summary statistics, e.g.:
                    -- { "mean_delta_temp_k": -0.8, "max_delta_aqi": -12, "r_squared": 0.94 }
    computed_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    model_version   VARCHAR(64) NOT NULL            -- e.g. 'pinn_v0.3.1_torchscript'
);

COMMENT ON TABLE scenario_results IS
    'Stores PINN model predictions for each scenario. result_grid contains '
    'per-grid-cell predicted deltas, uncertainty holds confidence intervals, '
    'and metrics provides aggregate summary statistics.';

-- ==========================================================================
-- 7. SPATIAL INDICES (GIST) — on all geometry columns
-- ==========================================================================
CREATE INDEX idx_climate_observations_geom ON climate_observations USING GIST (geom);
CREATE INDEX idx_climate_grid_geom         ON climate_grid         USING GIST (geom);
CREATE INDEX idx_climate_grid_centroid      ON climate_grid         USING GIST (centroid);
CREATE INDEX idx_planning_zones_geom       ON planning_zones       USING GIST (geom);

-- ==========================================================================
-- 8. B-TREE INDICES — for common query patterns
-- ==========================================================================
CREATE INDEX idx_observations_dataset      ON climate_observations (dataset);
CREATE INDEX idx_observations_observed_at  ON climate_observations (observed_at);
CREATE INDEX idx_observations_grid_cell    ON climate_observations (grid_cell_id);
CREATE INDEX idx_scenarios_status          ON scenarios (status);
CREATE INDEX idx_scenarios_zone_id         ON scenarios (zone_id);
CREATE INDEX idx_scenario_results_scenario ON scenario_results (scenario_id);
