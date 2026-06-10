from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from logging.handlers import RotatingFileHandler

import logging
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

load_dotenv('.env')


def load_to_sql(df: pd.DataFrame):

    try:
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        DB_NAME = os.getenv("DB_NAME")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")

        if not all([DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD]):
            raise ValueError("Missing one or more database environment variables.")

        DB_PASSWORD = quote_plus(DB_PASSWORD)

        # Database URL
        DATABASE_URL = (
            f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
            f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

        # Database URL * For Local MySQL
        #   DATABASE_URL = (
        #             f"mysql+mysqldb://{DB_USER}:{DB_PASSWORD}"
        #             f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        #         )

        # Create engine
        engine = create_engine(DATABASE_URL)

        # Load DataFrame
        df.to_sql(
            name="transaction_data",
            con=engine,
            if_exists="replace",
            index=False
        )

        logger.info("Transaction data loaded successfully.")
        print("Successfully loaded transaction data to database.")

    except Exception as e:
        logger.exception(f"Error loading data to PostgreSQL:{e}")
        print(f"Error loading data to PostgreSQL: Check logs for more information")