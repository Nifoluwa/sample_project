import streamlit as st
import pandas as pd
from babel.numbers import format_decimal

from help import data_computations, get_data, init_state, render_filters, integer_metric_card, currency_metric_card

df = get_data()

init_state()

st.title("Transaction Data Dashboard")

type_categories = ["All"] + list(df["Transaction Type"].unique())

device_used = ["All"] + list(df["Device Used"].unique())

min_date, max_date = df["Transaction Date"].min(), df["Transaction Date"].max()

transaction_filter = render_filters(picker=type_categories, device=device_used, start_date=min_date, end_date=max_date)

metrics = data_computations(df, transaction_filter["picker"], transaction_filter["device"], transaction_filter["start_date"], transaction_filter["end_date"])

current_metrics = data_computations(
    df,
    st.session_state.picker,
    st.session_state.device,
    st.session_state.start_date,
    st.session_state.end_date
)

if "previous_metrics" not in st.session_state:
    st.session_state.previous_metrics = current_metrics.copy()


transaction_delta = (
    current_metrics["transaction_number"]
    - st.session_state.previous_metrics["transaction_number"]
)

volume_delta = (
    current_metrics["transaction_volume"]
    - st.session_state.previous_metrics["transaction_volume"]
)

daily_delta = (
    current_metrics["average_daily_transactions"]
    - st.session_state.previous_metrics["average_daily_transactions"]
)

monthly_delta = (
    current_metrics["average_monthly_transactions"]
    - st.session_state.previous_metrics["average_monthly_transactions"]
)

user_delta = (
    current_metrics["user_count"]
    -st.session_state.previous_metrics["user_count"]
)


col1, col2, col3 = st.columns([1, 1.5, 1])

with col1:
    integer_metric_card(
        "Total Transactions",
        metrics["transaction_number"],
        transaction_delta
    )

with col2:
    currency_metric_card(
        "Total Transaction Volume",
        metrics['transaction_volume'],
        volume_delta
    )

with col3:
    integer_metric_card(
        "Total Users Served",
        metrics["user_count"],
        user_delta
    )
col4, col5, col6 = st.columns([1, 1.5, 1])
with col4:
    integer_metric_card(
        "Average Daily Transactions",
    metrics["average_daily_transactions"],
        daily_delta
    )

with col5:
    integer_metric_card(
        "Average Monthly Transactions",
    metrics["average_monthly_transactions"],
        monthly_delta
    )
with col6:
    integer_metric_card(
        "Fraudulent Transactions(%)",
        metrics["fraud_pct"],
    )