import asyncio
import logging
from datetime import datetime

from .cpcb_fetcher import fetch_cpcb_aq
from .db_writer import write_observations
from .gee_fetcher import fetch_gee_data
from .grid_fuser import resample_raster_to_grid
from .imd_fetcher import fetch_imd_stations
from .mosdac_fetcher import fetch_mosdac_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_pipeline():
    date = "2026-07-07"
    bbox = {
        "min_lon": 78.0,
        "min_lat": 17.0,
        "max_lon": 79.0,
        "max_lat": 18.0
    }
    observed_at = datetime.strptime(date, "%Y-%m-%d")

    logger.info("Starting ingest pipeline...")

    # Fetch Data
    gee_files = fetch_gee_data("lst", date, bbox)
    mosdac_files = fetch_mosdac_data(date, bbox)
    imd_data = fetch_imd_stations(date, bbox)
    cpcb_data = fetch_cpcb_aq(date, bbox)

    # Process and write GEE data
    for f in gee_files:
        grid_data = resample_raster_to_grid(f, bbox)
        await write_observations("gee_lst", observed_at, grid_data)

    # Process and write MOSDAC data
    for f in mosdac_files:
        grid_data = resample_raster_to_grid(f, bbox)
        await write_observations("mosdac", observed_at, grid_data)

    # Write IMD and CPCB data directly
    await write_observations("imd_stations", observed_at, imd_data)
    await write_observations("cpcb_aq", observed_at, cpcb_data)

    logger.info("Ingest pipeline completed.")

if __name__ == "__main__":
    asyncio.run(run_pipeline())
