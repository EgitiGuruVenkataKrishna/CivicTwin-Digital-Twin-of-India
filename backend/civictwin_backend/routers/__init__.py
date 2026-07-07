"""CivicTwin API routers – public API surface.

All four domain routers are imported and re-exported here so that
``main.py`` can mount them with a single import:

    from civictwin_backend.routers import climate_router, zones_router, ...
"""

from civictwin_backend.routers.climate import router as climate_router
from civictwin_backend.routers.inference import router as inference_router
from civictwin_backend.routers.scenarios import router as scenarios_router
from civictwin_backend.routers.zones import router as zones_router

__all__ = [
    "climate_router",
    "inference_router",
    "scenarios_router",
    "zones_router",
]
