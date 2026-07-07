"""CivicTwin Backend — Climate data ORM models.

Stores raw climate observations (point measurements) and the spatial grid
used for aggregation and PINN input/output.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import DateTime, Integer, JSON, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from civictwin_backend.database import Base


class ClimateObservation(Base):
    """A single climate measurement (temperature, humidity, AQI, etc.).

    Each observation is georeferenced as a POINT and optionally linked to a
    grid cell for spatial aggregation.
    """

    __tablename__ = "climate_observations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    dataset: Mapped[str] = mapped_column(String, nullable=False, index=True)
    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    geom: Mapped[str] = mapped_column(
        Geometry("POINT", srid=4326), nullable=False
    )
    properties: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    grid_cell_id: Mapped[str | None] = mapped_column(
        String, nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class ClimateGrid(Base):
    """A spatial grid cell (e.g. 250 m × 250 m) covering the pilot city.

    The grid acts as the spatial backbone for PINN inputs / outputs and
    front-end map tiles.
    """

    __tablename__ = "climate_grid"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    cell_id: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True
    )
    geom: Mapped[str] = mapped_column(
        Geometry("POLYGON", srid=4326), nullable=False
    )
    centroid: Mapped[str] = mapped_column(
        Geometry("POINT", srid=4326), nullable=True
    )
    resolution_m: Mapped[int] = mapped_column(Integer, default=250)
    metadata_: Mapped[dict | None] = mapped_column(
        "metadata", JSON, nullable=True
    )
