from .climate import router as climate_router
from .inference import router as inference_router
from .scenarios import router as scenarios_router
from .simulation import router as simulation_router
from .zones import router as zones_router

__all__ = [
    "climate_router",
    "zones_router",
    "scenarios_router",
    "inference_router",
    "simulation_router",
]
