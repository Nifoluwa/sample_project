import logging
from datetime import datetime
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
from etl_pipeline import extract, transform, load

def main(filepath: str):
    try:
        print("Extracting data....")
        file = extract.extract(filepath)
        print("Transforming data....")
        df = transform.transformer(file)
        load.load_to_sql(df)
    except Exception as error:
        logging.exception(f"{datetime.now()}:{error}")
        print("Error executing pipeline. Check logs for more information.")

if __name__ == "__main__":
    main("datasets/transaction_data.csv")