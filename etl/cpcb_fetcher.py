import logging

logger = logging.getLogger(__name__)

def fetch_cpcb_aq(date: str, bbox: dict) -> list[dict]:
    """
    Fetch data from CPCB.
    """
    logger.info("Fetching mock CPCB AQ data")
    return [
        {"lat": 17.38, "lon": 78.48, "properties": {"aqi": 45, "pm25": 12.5}}
    ]
