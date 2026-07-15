import logging
import os
import sys
from datetime import datetime

# Add backend directory to path to allow importing civictwin_backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from civictwin_backend.database import async_session
from civictwin_backend.models.climate import ClimateObservation
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

logger = logging.getLogger(__name__)

async def write_observations(dataset: str, observed_at: datetime, observations: list[dict]) -> None:
    """
    Write observations to the database.
    """
    async with async_session() as db:
        try:
            records = []
            for obs in observations:
                lat = obs.get("lat")
                lon = obs.get("lon")
                properties = obs.get("properties", {})

                if lat is None or lon is None:
                    continue

                point = Point(lon, lat)
                geom = from_shape(point, srid=4326)

                record = ClimateObservation(
                    dataset=dataset,
                    observed_at=observed_at,
                    geom=geom,
                    properties=properties
                )
                records.append(record)

            db.add_all(records)
            await db.commit()
            logger.info(f"Successfully wrote {len(records)} observations for {dataset}.")
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to write observations: {e}")
