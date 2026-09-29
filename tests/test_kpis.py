"""Unit tests for the data + KPI layer (UI is not tested here — logic is)."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import data  # noqa: E402


def test_schema_and_size():
    df = data.load_data(n_days=30)
    assert set(df.columns) == {"date", "product", "channel", "units", "revenue"}
    # 30 days × 4 products × 3 channels
    assert len(df) == 30 * len(data.PRODUCTS) * len(data.CHANNELS)


def test_no_negative_values():
    df = data.load_data(n_days=60)
    assert (df["units"] >= 1).all()
    assert (df["revenue"] >= 0).all()


def test_deterministic():
    a = data.load_data(n_days=45)
    b = data.load_data(n_days=45)
    pd.testing.assert_frame_equal(a, b)  # seeded -> identical every run


def test_kpis_consistent():
    df = data.load_data(n_days=90)
    k = data.compute_kpis(df)
    assert k["revenue"] > 0
    assert k["units"] > 0
    assert k["top_product"] in set(df["product"])
    assert k["top_channel"] in set(df["channel"])
    assert k["n_rows"] == len(df)


def test_revenue_equals_sum():
    df = data.load_data(n_days=30)
    k = data.compute_kpis(df)
    assert abs(k["revenue"] - df["revenue"].sum()) < 1e-6


def test_avg_order_value_identity():
    df = data.load_data(n_days=30)
    k = data.compute_kpis(df)
    assert abs(k["avg_order_value"] - k["revenue"] / k["units"]) < 1e-6


def test_avg_daily_revenue_matches_grouping():
    df = data.load_data(n_days=30)
    k = data.compute_kpis(df)
    expected = df.groupby("date")["revenue"].sum().mean()
    assert abs(k["avg_daily_revenue"] - expected) < 1e-6


def test_filtered_subset_never_exceeds_total():
    df = data.load_data(n_days=60)
    total = data.compute_kpis(df)["revenue"]
    sub = data.compute_kpis(df[df["channel"] == "Online"])["revenue"]
    assert 0 < sub < total


def test_empty_frame_is_safe():
    df = data.load_data(n_days=10)
    k = data.compute_kpis(df.iloc[0:0])
    assert k["revenue"] == 0.0
    assert k["units"] == 0
    assert k["top_product"] == "—"
