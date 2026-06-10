import pandas as pd
import streamlit as st
from babel.numbers import format_decimal


months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October"]

@st.cache_resource
def get_data():
    conn = st.connection("env:DB_CONN", "sql")

    df = conn.query("SELECT * FROM transaction_data")

    return df

def init_state():
    defaults = {
        "picker": "All",
        "device": "All",
        "start_date":None,
        "end_date":None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

@st.cache_data
def data_computations(data:pd.DataFrame, selection_one, selection_two, selection_three, selection_four):
    if selection_one != "All":
        data = data[data["Transaction Type"] == selection_one]

    if selection_two != "All":
        data = data[data["Device Used"] == selection_two]

    if selection_three is not None:
        data = data[data["Transaction Date"] >= selection_three]

    if selection_four is not None:
        data = data[data["Transaction Date"] <= selection_four]

    if data.empty:
        return {
            "transaction_number": 0,
            "transaction_volume": 0,
            "fraud_pct": 0,
            "amount_by_device": pd.DataFrame(),
            "transaction_types": pd.DataFrame(),
            "user_count": 0,
            "average_daily_transactions": 0,
            "average_monthly_transactions": 0,
        }


    transaction_number = data.shape[0]
    transaction_volume = data["Transaction Amount"].sum()
    fraud_pct = round(data["Fraud Flag"].value_counts(normalize=True).iloc[1] * 100, 2)
    transaction_types = data.pivot_table(["Transaction Amount"], "Transaction Type", aggfunc="sum")
    amount_by_device = data.pivot_table(["Transaction Amount"], "Device Used", aggfunc="sum")
    receivers, senders = set(data["Receiver Account ID"]), set(data["Sender Account ID"])
    user_count = len(receivers & senders) + len(receivers.symmetric_difference(senders))
    average_daily_transactions = int(data.shape[0]/len(set(data["Transaction Date"].unique())))
    average_monthly_transactions = int(data.shape[0]/len(set(data["Transaction Month"].unique())))

    return {"transaction_number": transaction_number,
            "transaction_volume": transaction_volume,
            "fraud_pct": fraud_pct,
            "amount_by_device": amount_by_device,
            "transaction_types": transaction_types,
            "user_count": user_count,
            "average_daily_transactions": average_daily_transactions,
            "average_monthly_transactions": average_monthly_transactions}


@st.cache_data
def graph_computations(data: pd.DataFrame, selection_one, selection_two, selection_three, selection_four):
    if selection_one != "All":
        data = data[data["Transaction Type"] == selection_one]

    if selection_two != "All":
        data = data[data["Device Used"] == selection_two]

    if selection_three is not None:
        data = data[data["Transaction Date"] >= selection_three]

    if selection_four is not None:
        data = data[data["Transaction Date"] <= selection_four]

    transaction_types = data.pivot_table(["Transaction Amount"], "Transaction Type", aggfunc="sum")
    month_groups = data.groupby("Transaction Month")
    ordered_months = month_groups.size().reindex(months)
    amount_by_device = data.pivot_table(["Transaction Amount"], "Device Used", aggfunc="sum")
    fraud_pct = data["Fraud Flag"].value_counts(normalize=True)
    success_status = data["Transaction Status"].value_counts(normalize=True)

    return {"transaction_types":transaction_types,
            "ordered_months":ordered_months,
            "amount_by_device":amount_by_device,
            "fraud_flag":fraud_pct,
            "success_status":success_status}


def render_filters(**kwargs):
    if kwargs["picker"] and kwargs["device"] and kwargs["start_date"] and kwargs["end_date"]:
        st.session_state.picker = st.sidebar.selectbox(
            "Transaction Type",
            options=kwargs["picker"],
            index=kwargs["picker"].index(st.session_state.picker)
            if st.session_state.picker in kwargs["picker"] else 0,
            key="transaction_type_filter")
        st.session_state.device = st.sidebar.selectbox(
            "Device Used",
            options=kwargs["device"],
            index=kwargs["device"].index(st.session_state.device),
            key="device_type_filter")
        st.session_state.start_date = st.sidebar.slider(
            "Start Date",
            min_value=kwargs["start_date"],
            max_value=kwargs["end_date"],
            value=kwargs["start_date"]
        )
        st.session_state.end_date = st.sidebar.slider(
            "End Date",
            min_value=kwargs["start_date"],
            max_value=kwargs["end_date"],
            value=kwargs["end_date"]
        )

        return {"picker":st.session_state.picker,
                "device":st.session_state.device,
                "start_date":st.session_state.start_date,
                "end_date":st.session_state.end_date}

    return None

def integer_metric_card(title, value, delta=None):
    st.metric(border=True, label=title, value=format_decimal(value, locale="en_US"), delta=delta)

def currency_metric_card(title, value, delta=None):
    st.metric(border=True, label=title, value=0 if value == 0 else f"${value:,.2f}", delta=format_decimal(delta))