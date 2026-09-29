"""Interactive sales KPI dashboard — run with: streamlit run app.py

The data/KPI logic lives in ``data.py`` (importable + unit-tested); this module is
the presentation layer only.
"""
import altair as alt
import pandas as pd
import streamlit as st

from data import load_data, compute_kpis

PALETTE = ["#1E90FF", "#00C2A8", "#F5A524", "#7C5CFF", "#F2647C"]

st.set_page_config(page_title="Sales KPI Dashboard", page_icon="📊", layout="wide")


@st.cache_data
def _data() -> pd.DataFrame:
    # Cached so filter interactions never regenerate the dataset.
    return load_data()


st.title("📊 Sales KPI Dashboard")
st.caption("Interactive analytics web app — synthetic multi-channel sales, "
           "filterable KPIs, and drill-down charts.")

df = _data()

with st.sidebar:
    st.header("Filters")
    products = st.multiselect("Product", sorted(df["product"].unique()),
                              default=sorted(df["product"].unique()))
    channels = st.multiselect("Channel", sorted(df["channel"].unique()),
                              default=sorted(df["channel"].unique()))
    date_range = st.date_input("Date range", [df["date"].min(), df["date"].max()])
    st.markdown("---")
    st.caption("Data is synthetic and seeded — the same every run.")

mask = df["product"].isin(products) & df["channel"].isin(channels)
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    mask &= df["date"].between(pd.Timestamp(date_range[0]),
                               pd.Timestamp(date_range[1]))
fdf = df[mask]

k = compute_kpis(fdf)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"${k['revenue']:,.0f}")
c2.metric("Total Units", f"{k['units']:,}")
c3.metric("Avg Order Value", f"${k['avg_order_value']:,.2f}")
c4.metric("Top Product", k["top_product"])

c5, c6, c7, c8 = st.columns(4)
c5.metric("Avg Daily Revenue", f"${k['avg_daily_revenue']:,.0f}")
c6.metric("Top Channel", k["top_channel"])
c7.metric("Best Day", k["best_day"])
c8.metric("Rows in view", f"{k['n_rows']:,}")

st.markdown("---")

st.subheader("Revenue Over Time")
ts = fdf.groupby("date", as_index=False)["revenue"].sum()
line = (alt.Chart(ts)
        .mark_area(line={"color": PALETTE[0]}, color=alt.Gradient(
            gradient="linear",
            stops=[alt.GradientStop(color="#1E90FF", offset=0),
                   alt.GradientStop(color="white", offset=1)],
            x1=1, x2=1, y1=1, y2=0))
        .encode(x=alt.X("date:T", title=None),
                y=alt.Y("revenue:Q", title="Revenue"))
        .properties(height=280))
st.altair_chart(line, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Revenue by Product")
    by_p = fdf.groupby("product", as_index=False)["revenue"].sum()
    chart = (alt.Chart(by_p)
             .mark_bar()
             .encode(x=alt.X("product:N", sort="-y", title=None),
                     y=alt.Y("revenue:Q", title="Revenue"),
                     color=alt.Color("product:N", scale=alt.Scale(range=PALETTE),
                                     legend=None))
             .properties(height=280))
    st.altair_chart(chart, use_container_width=True)
with right:
    st.subheader("Revenue by Channel")
    by_c = fdf.groupby("channel", as_index=False)["revenue"].sum()
    chart = (alt.Chart(by_c)
             .mark_bar()
             .encode(x=alt.X("channel:N", sort="-y", title=None),
                     y=alt.Y("revenue:Q", title="Revenue"),
                     color=alt.Color("channel:N", scale=alt.Scale(range=PALETTE),
                                     legend=None))
             .properties(height=280))
    st.altair_chart(chart, use_container_width=True)

st.subheader("Detail")
st.dataframe(fdf.sort_values("date").head(500), use_container_width=True)
