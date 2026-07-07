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
    """Create all tables defined on `Base.metadata`.

    Only used for local development.  Production uses Alembic migrations.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created (dev mode).")
