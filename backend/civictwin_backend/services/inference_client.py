"""Async inference client for the HF Space PINN model.

This module is the **DECOUPLED bridge** between the FastAPI backend and
the ML model hosted on Hugging Face Spaces.  The backend NEVER imports
``torch`` — all inference traffic flows through this ``httpx``-based
HTTP client.

Handles:
* Configurable base URL + optional bearer token
* Timeouts  (30 s default)
* Automatic retries with exponential back-off (3 attempts)
* Graceful error handling → ``HTTPException`` bubbling
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx
from fastapi import HTTPException

from civictwin_backend.config import get_settings
from civictwin_backend.schemas.scenario import InferenceRequest, InferenceResponse

logger = logging.getLogger(__name__)

_DEFAULT_TIMEOUT = 30.0  # seconds
_MAX_RETRIES = 3
_BACKOFF_BASE = 1.5  # seconds – multiplied by attempt index


class InferenceClient:
    """Async HTTP client wrapping the HF Space inference API."""

    def __init__(
        self,
        base_url: str,
        token: str | None = None,
        timeout: float = _DEFAULT_TIMEOUT,
    ) -> None:
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers=headers,
            timeout=httpx.Timeout(timeout),
        )
        self._base_url = base_url

    # ── Inference ───────────────────────────────────────────────────────

    async def predict(
        self,
        grid_data: list[dict[str, Any]],
        scenario_params: dict[str, Any],
        model_version: str = "latest",
    ) -> InferenceResponse:
        """POST to ``{base_url}/predict`` and return parsed predictions."""
        payload = InferenceRequest(
            grid_data=grid_data,
            scenario_params=scenario_params,
            model_version=model_version,
        ).model_dump()

        data = await self._request_with_retry("POST", "/predict", json=payload)
        return InferenceResponse(**data)

    # ── Health / metadata ───────────────────────────────────────────────

    async def health_check(self) -> bool:
        """Return ``True`` if the HF Space is reachable and healthy."""
        try:
            await self._request_with_retry("GET", "/health")
            return True
        except Exception:
            return False

    async def get_model_info(self) -> dict[str, Any]:
        """Return model metadata from the HF Space."""
        return await self._request_with_retry("GET", "/model-info")

    # ── Lifecycle ───────────────────────────────────────────────────────

    async def close(self) -> None:
        """Shut down the underlying ``httpx.AsyncClient``."""
        await self._client.aclose()

    # ── Internal retry logic ────────────────────────────────────────────

    async def _request_with_retry(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Execute an HTTP request with exponential-backoff retries."""
        last_exc: Exception | None = None

        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                response = await self._client.request(method, path, **kwargs)
                response.raise_for_status()
                return response.json()

            except httpx.TimeoutException as exc:
                last_exc = exc
                logger.warning(
                    "HF Space timeout (attempt %d/%d): %s",
                    attempt,
                    _MAX_RETRIES,
                    exc,
                )
            except httpx.HTTPStatusError as exc:
                last_exc = exc
                # Don't retry client errors (4xx)
                if 400 <= exc.response.status_code < 500:
                    raise HTTPException(
                        status_code=exc.response.status_code,
                        detail=f"HF Space returned {exc.response.status_code}: "
                        f"{exc.response.text[:500]}",
                    )
                logger.warning(
                    "HF Space HTTP %d (attempt %d/%d)",
                    exc.response.status_code,
                    attempt,
                    _MAX_RETRIES,
                )
            except httpx.HTTPError as exc:
                last_exc = exc
                logger.warning(
                    "HF Space request error (attempt %d/%d): %s",
                    attempt,
                    _MAX_RETRIES,
                    exc,
                )

            if attempt < _MAX_RETRIES:
                await asyncio.sleep(_BACKOFF_BASE * attempt)

        raise HTTPException(
            status_code=502,
            detail=f"HF Space unreachable after {_MAX_RETRIES} retries: {last_exc}",
        )


# ── Module-level factory ────────────────────────────────────────────────

_singleton: InferenceClient | None = None


def get_inference_client() -> InferenceClient:
    """Return a module-level ``InferenceClient`` configured from settings.

    The client is created once and reused across the application lifetime.
    """
    global _singleton
    if _singleton is None:
        settings = get_settings()
        _singleton = InferenceClient(
            base_url=settings.HF_SPACE_URL,
            token=settings.HF_TOKEN,
        )
    return _singleton
