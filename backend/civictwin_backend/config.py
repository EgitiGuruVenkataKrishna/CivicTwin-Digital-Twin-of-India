"""CivicTwin Backend — Application configuration.

Reads environment variables (or .env file) using pydantic-settings.
All defaults are tuned for local development; override via env in production.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for the CivicTwin API.

    Bharatiya Antariksh Hackathon 2026 | Team CivicTwin
    Pilot city: Hyderabad
    """

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env", "../infra/.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Database (Supabase PostGIS via asyncpg) ──────────────────────────
    DATABASE_URL: str = (
        "postgresql+asyncpg://civictwin:civictwin_dev@localhost:5432/civictwin"
    )
    DATABASE_URL_SYNC: str = (
        "postgresql://civictwin:civictwin_dev@localhost:5432/civictwin"
    )

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str | None) -> str:
        if isinstance(v, str):
            if v.startswith("postgres://"):
                return v.replace("postgres://", "postgresql+asyncpg://", 1)
            if v.startswith("postgresql://"):
                return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v or "postgresql+asyncpg://civictwin:civictwin_dev@localhost:5432/civictwin"

    # ── Redis (caching / pub-sub) ────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── Hugging Face Spaces (PINN inference endpoint) ────────────────────
    HF_SPACE_URL: str = "http://localhost:7860"
    HF_TOKEN: str | None = None

    # ── CORS ─────────────────────────────────────────────────────────────
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    # ── Server ───────────────────────────────────────────────────────────
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    # ── Supabase ─────────────────────────────────────────────────────────
    SUPABASE_URL: str | None = None
    SUPABASE_ANON_KEY: str | None = None

    # ── Google Earth Engine ──────────────────────────────────────────────
    GEE_SERVICE_ACCOUNT_EMAIL: str | None = None

    # ── Project metadata ─────────────────────────────────────────────────
    PROJECT_NAME: str = "CivicTwin API"
    VERSION: str = "0.1.0"
    PILOT_CITY: str = "Hyderabad"
    PILOT_BBOX: dict[str, float] = {
        "west": 78.2,
        "south": 17.2,
        "east": 78.7,
        "north": 17.6,
    }


# Module-level singleton — imported across the application.
settings = Settings()


@lru_cache
def get_settings() -> Settings:
    """FastAPI dependency that returns the cached Settings instance."""
    return settings
