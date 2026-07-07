"""CivicTwin Backend — Scenario & result ORM models.

A Scenario represents a what-if intervention (e.g. "add 500 trees in zone X")
and its parameters.  ScenarioResult stores the PINN output grids, uncertainty
maps, and summary metrics after inference.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from civictwin_backend.database import Base


class Scenario(Base):
    """A what-if scenario tied to a specific planning zone."""

    __tablename__ = "scenarios"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    zone_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("planning_zones.id"),
        nullable=False,
        index=True,
    )
    intervention_type: Mapped[str] = mapped_column(
        String, nullable=False, index=True,
        comment="e.g. afforestation, cool_roof, water_body, traffic_reduction",
    )
    parameters: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(
        String, nullable=False, default="pending", index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # ── Relationships ────────────────────────────────────────────────────
    zone = relationship("PlanningZone", backref="scenarios", lazy="selectin")
    results: Mapped[list["ScenarioResult"]] = relationship(
        back_populates="scenario",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class ScenarioResult(Base):
    """Inference output from the PINN model for a given scenario."""

    __tablename__ = "scenario_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    scenario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scenarios.id"),
        nullable=False,
        index=True,
    )
    result_grid: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    uncertainty: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    metrics: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    computed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    model_version: Mapped[str | None] = mapped_column(String, nullable=True)

    # ── Relationships ────────────────────────────────────────────────────
    scenario: Mapped["Scenario"] = relationship(back_populates="results")
