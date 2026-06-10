import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from help import data_computations, get_data, init_state, render_filters, graph_computations

df = get_data()

init_state()

device_used = ["All"] + list(df["Device Used"].unique())

type_categories = ["All"] + list(df["Transaction Type"].unique())

min_date, max_date = df["Transaction Date"].min(), df["Transaction Date"].max()

transaction_filter = render_filters(picker=type_categories, device=device_used, start_date=min_date, end_date=max_date)

metric = graph_computations(df, transaction_filter["picker"], transaction_filter["device"], transaction_filter["start_date"], transaction_filter["end_date"])

left_column, right_column = st.columns([2, 2])
with left_column:
    with st.container(border=True):
        fig = px.bar(
            metric["transaction_types"], title="Volumes By Transactions Types")

        st.plotly_chart(fig, use_container_width=True)


with right_column:
    with st.container(border=True):
        fig = px.line(
            metric["ordered_months"] ,y=metric["ordered_months"].values, labels={"y":"Transaction Volume"},
            title="Transaction Volumes By Month")

        st.plotly_chart(fig, use_container_width=True)

left_column_two, right_column_two = st.columns([2, 2])
with left_column_two:
    with st.container(border=True):
        fig = px.pie(
                values = metric["fraud_flag"],
                hover_name={"x":"Non-Fraudulent", "y":"Fraudulent"},
                title="Fraudulent Transactions(%)")

        st.plotly_chart(fig, use_container_width=True)
with right_column_two:
    with st.container(border=True):
        fig = px.pie(
            values=metric["success_status"],
            hover_name={"x": "Non-Fraudulent", "y": "Fraudulent"},
            title="Successful Transactions(%)")

        st.plotly_chart(fig, use_container_width=True)

ID = st.text_input("Enter a transaction ID:")

st.dataframe(df[df["Transaction ID"] == ID ])

date = st.date_input("Enter a transaction date (YY-MM-DD):")

st.dataframe(df[df["Transaction Date"] == date])