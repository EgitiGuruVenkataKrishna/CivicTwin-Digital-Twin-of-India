"""CivicTwin Pydantic schemas – public API surface.

All schema classes are re-exported here so consumers can do:

    from civictwin_backend.schemas import ClimateSnapshotResponse, ZoneOut
"""

from civictwin_backend.schemas.climate import (
    BBox,
    ClimateObservationOut,
    ClimateSnapshotRequest,
    ClimateSnapshotResponse,
    TimeseriesPoint,
    TimeseriesRequest,
    TimeseriesResponse,
)
from civictwin_backend.schemas.scenario import (
    InferenceRequest,
    InferenceResponse,
    ScenarioCreate,
    ScenarioOut,
    ScenarioResultOut,
)
from civictwin_backend.schemas.zone import (
    ZoneCreate,
    ZoneOut,
    ZoneUpdate,
)

__all__ = [
    # climate
    "BBox",
    "ClimateObservationOut",
    "ClimateSnapshotRequest",
    "ClimateSnapshotResponse",
    "TimeseriesPoint",
    "TimeseriesRequest",
    "TimeseriesResponse",
    # zone
    "ZoneCreate",
    "ZoneOut",
    "ZoneUpdate",
    # scenario
    "InferenceRequest",
    "InferenceResponse",
    "ScenarioCreate",
    "ScenarioOut",
    "ScenarioResultOut",
]
