"""CivicTwin services – public API surface.

Re-exports the main service functions and classes so consumers can do:

    from civictwin_backend.services import get_inference_client
    from civictwin_backend.services import climate_service
"""

from civictwin_backend.services.climate_service import (
    get_latest_by_dataset,
    get_snapshot,
    get_timeseries,
)
from civictwin_backend.services.inference_client import (
    InferenceClient,
    get_inference_client,
)
from civictwin_backend.services.scenario_service import (
    create_scenario,
    get_scenario,
    list_scenarios,
    run_scenario,
)

__all__ = [
    # climate
    "get_latest_by_dataset",
    "get_snapshot",
    "get_timeseries",
    # inference
    "InferenceClient",
    "get_inference_client",
    # scenario
    "create_scenario",
    "get_scenario",
    "list_scenarios",
    "run_scenario",
]
