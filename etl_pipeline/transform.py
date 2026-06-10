import pandas as pd
import logging
from logging.handlers import RotatingFileHandler

from pandas import DataFrame

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


from warnings import filterwarnings
filterwarnings(action="ignore")
from datetime import datetime


def transformer(df: pd.DataFrame) -> DataFrame | None:
    """Transform given data into proper form"""
    try:
        df.drop_duplicates(inplace=True)
        df["Device Used"].replace({"Deskto": "Desktop", "Mobil": "Mobile"}, inplace=True)
        df["Transaction Status"].replace({"Faile": "Failed", "Succes": "Success"}, inplace=True)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df.insert(7, "Transaction Date", df["Timestamp"].dt.date)
        df.insert(8, "Transaction Time", df["Timestamp"].dt.time)
        df.insert(9, "Transaction Month", df["Timestamp"].dt.month)
        df.replace({"Transaction Month": {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
                                            7: "July", 8: "August", 9: "September", 10: "October", 11: "November",
                                            12: "December"}}, inplace=True)

        for i in range(df.shape[0]):
            for r in (("N", ""), ("W", "")):
                df["Geolocation (Latitude/Longitude)"].iloc[i] = df["Geolocation (Latitude/Longitude)"].iloc[
                    i].replace(*r)
        df.insert(12, "longitude",[float(df["Geolocation (Latitude/Longitude)"][i].split()[0]) for i in range(df.shape[0])])
        df.insert(13, "latitude",[float(df["Geolocation (Latitude/Longitude)"][i].split()[-1]) for i in range(df.shape[0])])
        return df
    except Exception as error:
        logging.exception(f"{datetime.now()}:{error}")
        print("Error in transformation process. Check log file for more information.")