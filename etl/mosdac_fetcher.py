import os
import logging

logger = logging.getLogger(__name__)

def fetch_mosdac_data(date: str, bbox: dict) -> list[str]:
    """
    Fetch data from MOSDAC.
    """
    username = os.getenv("MOSDAC_USERNAME")
    password = os.getenv("MOSDAC_PASSWORD")
    
    if not username or not password:
        logger.warning("MOSDAC credentials missing. Returning mock data.")
        return ["data/raw/mosdac_mock.tif"]
        
    try:
        # Fetch logic here
        return [f"data/raw/mosdac_{date}.tif"]
    except Exception as e:
        logger.error(f"Error fetching MOSDAC data: {e}")
        return ["data/raw/mosdac_mock.tif"]
