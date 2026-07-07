"""CivicTwin Backend — Planning zone ORM model.

Represents administrative or planning zones in the pilot city.
Each zone has a polygon geometry and a type classification.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import DateTime, Float, JSON, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from civictwin_backend.database import Base


class PlanningZone(Base):
    """A planning / land-use zone within the pilot city.

    Zone types: residential, commercial, industrial, green_space, water_body.
    """

    __tablename__ = "planning_zones"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    zone_type: Mapped[str] = mapped_column(
        String, nullable=False, index=True,
        comment="residential | commercial | industrial | green_space | water_body",
    )
    geom: Mapped[str] = mapped_column(
        Geometry("POLYGON", srid=4326), nullable=False
    )
    area_sqkm: Mapped[float | None] = mapped_column(Float, nullable=True)
    properties: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
