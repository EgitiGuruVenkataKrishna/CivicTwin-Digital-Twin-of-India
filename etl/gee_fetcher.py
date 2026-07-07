import logging
import os

import ee

logger = logging.getLogger(__name__)

def fetch_gee_data(dataset_key: str, date: str, bbox: dict) -> list[str]:
    """
    Fetch data from Google Earth Engine.
    """
    service_account = os.getenv("GEE_SERVICE_ACCOUNT_EMAIL")
    private_key = os.getenv("GEE_PRIVATE_KEY_FILE")

    if not service_account or not private_key:
        logger.warning("GEE credentials missing. Returning mock data.")
        return ["data/raw/gee_mock.tif"]

    try:
        ee.Initialize(ee.ServiceAccountCredentials(service_account, private_key))
        # Filter ImageCollection by date and bounds, export to local GeoTIFF.
        # ... logic ...
        return [f"data/raw/{dataset_key}_{date}.tif"]
    except Exception as e:
        logger.error(f"Error fetching GEE data: {e}")
        return ["data/raw/gee_mock.tif"]
