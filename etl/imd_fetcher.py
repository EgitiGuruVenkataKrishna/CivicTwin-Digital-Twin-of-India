import logging

logger = logging.getLogger(__name__)

def fetch_imd_stations(date: str, bbox: dict) -> list[dict]:
    """
    Fetch data from IMD stations.
    """
    logger.info("Fetching mock IMD data")
    return [
        {"lat": 17.38, "lon": 78.48, "properties": {"temp_k": 300.15, "precip_mm": 0.0}}
    ]
