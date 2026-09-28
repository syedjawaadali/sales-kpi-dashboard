"""Data + KPI logic for the dashboard (kept separate from UI so it is testable)."""
import numpy as np
import pandas as pd

RNG = np.random.default_rng(5)


def load_data(n_days: int = 365) -> pd.DataFrame:
    dates = pd.date_range("2025-01-01", periods=n_days, freq="D")
    products = ["Alpha", "Bravo", "Charlie", "Delta"]
    channels = ["Online", "Retail", "Partner"]
    rows = []
    for d in dates:
        for p in products:
            for c in channels:
                units = RNG.integers(5, 60)
                revenue = round(units * RNG.uniform(15, 90), 2)
                rows.append((d, p, c, units, revenue))
    return pd.DataFrame(rows, columns=["date", "product", "channel",
                                       "units", "revenue"])


def compute_kpis(df: pd.DataFrame) -> dict:
    return {
        "revenue": float(df["revenue"].sum()),
        "units": int(df["units"].sum()),
        "avg_daily_revenue": float(df.groupby("date")["revenue"].sum().mean()),
        "top_product": df.groupby("product")["revenue"].sum().idxmax(),
    }
