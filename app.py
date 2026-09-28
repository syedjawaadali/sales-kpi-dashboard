"""Interactive sales KPI dashboard — run with: streamlit run app.py"""
import pandas as pd
import streamlit as st
from data import load_data, compute_kpis

st.set_page_config(page_title="Sales KPI Dashboard", layout="wide")
st.title("Sales KPI Dashboard")
st.caption("Interactive analytics web app — built by Syed Jawaad Ali")

df = load_data()

with st.sidebar:
    st.header("Filters")
    products = st.multiselect("Product", sorted(df["product"].unique()),
                              default=sorted(df["product"].unique()))
    channels = st.multiselect("Channel", sorted(df["channel"].unique()),
                              default=sorted(df["channel"].unique()))
    date_range = st.date_input("Date range",
                               [df["date"].min(), df["date"].max()])

mask = df["product"].isin(products) & df["channel"].isin(channels)
if len(date_range) == 2:
    mask &= df["date"].between(pd.Timestamp(date_range[0]),
                               pd.Timestamp(date_range[1]))
fdf = df[mask]

k = compute_kpis(fdf)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"${k['revenue']:,.0f}")
c2.metric("Total Units", f"{k['units']:,}")
c3.metric("Avg Daily Revenue", f"${k['avg_daily_revenue']:,.0f}")
c4.metric("Top Product", k["top_product"])

st.subheader("Revenue Over Time")
st.line_chart(fdf.groupby("date")["revenue"].sum())

left, right = st.columns(2)
with left:
    st.subheader("Revenue by Product")
    st.bar_chart(fdf.groupby("product")["revenue"].sum())
with right:
    st.subheader("Revenue by Channel")
    st.bar_chart(fdf.groupby("channel")["revenue"].sum())

st.subheader("Detail")
st.dataframe(fdf.head(500), use_container_width=True)
