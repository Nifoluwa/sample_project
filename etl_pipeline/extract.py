import pandas as pd
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    "etl_pipeline.log",
    maxBytes=5 * 1024 * 1024,
    backupCount=3
)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)

logger.addHandler(handler)

def extract(file_path: str):
    """Extract data from  file"""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        logger.exception(f"{datetime.now()}: {e}")