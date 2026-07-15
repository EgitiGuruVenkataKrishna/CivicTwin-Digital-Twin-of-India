"""CivicTwin Backend — Async database engine & session setup.

Uses SQLAlchemy 2.0 async engine backed by asyncpg, with GeoAlchemy2 for
PostGIS geometry columns.  Production migrations are handled by Alembic;
`init_db()` is provided for quick local development bootstrapping.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncGenerator

from geoalchemy2 import Geometry, WKBElement  # noqa: F401 — re-export for models
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from civictwin_backend.config import settings

logger = logging.getLogger(__name__)

# ── Async engine & session factory ───────────────────────────────────────
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=(settings.LOG_LEVEL == "DEBUG"),
    future=True,
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# ── Naming convention (keeps Alembic migrations deterministic) ───────────
NAMING_CONVENTION: dict[str, str] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


# ── Declarative Base ────────────────────────────────────────────────────
class Base(DeclarativeBase):
    """Base class for all ORM models.

    Includes a type_annotation_map so that `Geometry` columns are properly
    understood by SQLAlchemy's type system.
    """

    metadata = MetaData(naming_convention=NAMING_CONVENTION)
    type_annotation_map = {
        WKBElement: Geometry,
    }


# ── FastAPI dependency ──────────────────────────────────────────────────
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async DB session and ensure it is closed after the request."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ── Dev helper ──────────────────────────────────────────────────────────
async def init_db() -> None:
    """Create all tables defined on `Base.metadata` and seed default data.

    Only used for local development.  Production uses Alembic migrations.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created (dev mode).")

    # Seed default planning zones and observations if empty
    async with async_session() as session:
        try:
            from sqlalchemy import select, func
            from civictwin_backend.models.zone import PlanningZone
            from civictwin_backend.models.climate import ClimateObservation
            from datetime import datetime, UTC

            zone_check = await session.execute(select(PlanningZone).limit(1))
            if zone_check.scalar_one_or_none() is None:
                logger.info("🌱 Seeding default Hyderabad planning zones...")
                zones = [
                    PlanningZone(
                        name="Hussain Sagar",
                        zone_type="water_body",
                        geom=func.ST_GeomFromText("POLYGON((78.46 17.41, 78.48 17.41, 78.48 17.43, 78.46 17.43, 78.46 17.41))", 4326),
                        area_sqkm=4.0,
                        properties={"description": "Hussain Sagar lake and surrounding water features"},
                    ),
                    PlanningZone(
                        name="KBR National Park",
                        zone_type="green_space",
                        geom=func.ST_GeomFromText("POLYGON((78.41 17.41, 78.43 17.41, 78.43 17.43, 78.41 17.43, 78.41 17.41))", 4326),
                        area_sqkm=4.0,
                        properties={"description": "KBR National park and urban forest area"},
                    ),
                    PlanningZone(
                        name="HITEC City",
                        zone_type="commercial",
                        geom=func.ST_GeomFromText("POLYGON((78.37 17.43, 78.39 17.43, 78.39 17.45, 78.37 17.45, 78.37 17.43))", 4326),
                        area_sqkm=4.0,
                        properties={"description": "Commercial IT corridor and high-density offices"},
                    ),
                    PlanningZone(
                        name="Begumpet",
                        zone_type="residential",
                        geom=func.ST_GeomFromText("POLYGON((78.43 17.43, 78.45 17.43, 78.45 17.45, 78.43 17.45, 78.43 17.43))", 4326),
                        area_sqkm=4.0,
                        properties={"description": "Residential and mixed urban development"},
                    ),
                    PlanningZone(
                        name="Jeedimetla",
                        zone_type="industrial",
                        geom=func.ST_GeomFromText("POLYGON((78.43 17.47, 78.47 17.47, 78.47 17.51, 78.43 17.51, 78.43 17.47))", 4326),
                        area_sqkm=16.0,
                        properties={"description": "Industrial zone and manufacturing hub"},
                    ),
                ]
                session.add_all(zones)
                await session.commit()
                logger.info("   Planning zones seeded.")

            obs_check = await session.execute(select(ClimateObservation).limit(1))
            if obs_check.scalar_one_or_none() is None:
                logger.info("🌱 Seeding default climate observations...")
                # Add initial point observations for temperature and AQI
                obs = [
                    ClimateObservation(
                        dataset="cpcb_aq",
                        observed_at=datetime.now(UTC),
                        geom=func.ST_GeomFromText("POINT(78.47 17.42)", 4326),
                        properties={"value": 110.0, "uncertainty": 5.0, "aqi": 110.0, "temp_c": 32.5},
                    ),
                    ClimateObservation(
                        dataset="imd_stations",
                        observed_at=datetime.now(UTC),
                        geom=func.ST_GeomFromText("POINT(78.42 17.42)", 4326),
                        properties={"value": 31.0, "uncertainty": 0.5, "temp_c": 31.0},
                    ),
                    ClimateObservation(
                        dataset="gee_lst",
                        observed_at=datetime.now(UTC),
                        geom=func.ST_GeomFromText("POINT(78.38 17.44)", 4326),
                        properties={"value": 34.2, "uncertainty": 1.2, "temp_c": 34.2},
                    ),
                    ClimateObservation(
                        dataset="mosdac",
                        observed_at=datetime.now(UTC),
                        geom=func.ST_GeomFromText("POINT(78.44 17.44)", 4326),
                        properties={"value": 32.8, "uncertainty": 1.0, "temp_c": 32.8},
                    ),
                ]
                session.add_all(obs)
                await session.commit()
                logger.info("   Climate observations seeded.")

        except Exception as e:
            await session.rollback()
            logger.error("Failed to seed database: %s", e)

