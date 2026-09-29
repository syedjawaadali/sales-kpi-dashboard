"""Data + KPI logic for the dashboard.

Kept deliberately separate from the Streamlit UI so it is importable and unit-
testable. The generator is seeded per call, so the dashboard shows the same
numbers on every rerun (a filter interaction must not regenerate the data).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

PRODUCTS = ["Alpha", "Bravo", "Charlie", "Delta"]
CHANNELS = ["Online", "Retail", "Partner"]

# Structural multipliers so the analytics tell a story instead of showing noise.
_PRODUCT_MULT = {"Alpha": 1.35, "Bravo": 1.0, "Charlie": 0.8, "Delta": 0.6}
_CHANNEL_MULT = {"Online": 1.25, "Retail": 1.0, "Partner": 0.7}


def load_data(n_days: int = 365, seed: int = 5) -> pd.DataFrame:
    """Synthetic daily sales across products × channels with realistic structure:
    yearly seasonality, weekend uplift, and per-product / per-channel demand mix.
    """
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2025-01-01", periods=n_days, freq="D")

    day_idx = np.arange(n_days)
    season = 1 + 0.25 * np.sin(2 * np.pi * day_idx / 365)   # yearly cycle
    weekend = np.where(pd.Series(dates).dt.dayofweek >= 5, 1.18, 1.0)

    rows = []
    for i, d in enumerate(dates):
        demand = season[i] * weekend[i]
        for p in PRODUCTS:
            for c in CHANNELS:
                base = 30 * demand * _PRODUCT_MULT[p] * _CHANNEL_MULT[c]
                units = int(max(1, rng.normal(base, base * 0.25)))
                price = rng.uniform(15, 90)
                revenue = round(units * price, 2)
                rows.append((d, p, c, units, revenue))
    return pd.DataFrame(rows, columns=["date", "product", "channel",
                                       "units", "revenue"])


def compute_kpis(df: pd.DataFrame) -> dict:
    """Headline KPI set — the single source of truth for the metric cards."""
    if df.empty:
        return {"revenue": 0.0, "units": 0, "avg_daily_revenue": 0.0,
                "avg_order_value": 0.0, "top_product": "—", "top_channel": "—",
                "best_day": "—", "n_rows": 0}
    daily = df.groupby("date")["revenue"].sum()
    units = int(df["units"].sum())
    revenue = float(df["revenue"].sum())
    return {
        "revenue": revenue,
        "units": units,
        "avg_daily_revenue": float(daily.mean()),
        "avg_order_value": revenue / max(1, units),
        "top_product": df.groupby("product")["revenue"].sum().idxmax(),
        "top_channel": df.groupby("channel")["revenue"].sum().idxmax(),
        "best_day": str(daily.idxmax().date()),
        "n_rows": int(len(df)),
    }
