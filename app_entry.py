import streamlit as st
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    "application_logs.log",
    maxBytes=5 * 1024 * 1024,
    backupCount=3
)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)

logger.addHandler(handler)

st.set_page_config(layout="wide")

base_page = st.Page("main_page.py", title="Main Page")
visuals_page = st.Page("page_2.py", title="Visuals_Page")



st.sidebar.header("Filters")



pages = st.navigation([base_page, visuals_page])


pages.run()