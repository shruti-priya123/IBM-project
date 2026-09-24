# =============================================================================
# data_analysis.py
# =============================================================================
# Handles ALL data work for the E-Commerce Analytics project:
#   - Loading the CSV
#   - Cleaning and preprocessing
#   - Feature engineering  (Profit, Quantity, time columns)
#   - KPI calculations
#   - Aggregation functions used by the charts and AI engine
#
# DATASET NOTE:
#   The Superstore CSV contains only a "Sales" column — no Profit or Quantity.
#   We estimate Profit using realistic retail margin rates per category:
#       Technology      → 18%
#       Office Supplies → 14%
#       Furniture       → 6%
#   Quantity is estimated from typical sub-category order sizes.
# =============================================================================

import os
import pandas as pd
import numpy as np

# -----------------------------------------------------------------------------
# Path to the dataset  (always relative to this file, so it works from any CWD)
# -----------------------------------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "superstore.csv")

# -----------------------------------------------------------------------------
# Profit margin rates by category  (industry-standard retail estimates)
# -----------------------------------------------------------------------------
CATEGORY_MARGINS = {
    "Technology":      0.18,
    "Office Supplies": 0.14,
    "Furniture":       0.06,
}

# -----------------------------------------------------------------------------
# Average quantity (units) per order line by sub-category
# -----------------------------------------------------------------------------
SUB_CATEGORY_QUANTITY = {
    "Accessories": 3,
    "Appliances":  2,
    "Art":         8,
    "Binders":     6,
    "Bookcases":   2,
    "Chairs":      2,
    "Copiers":     1,
    "Envelopes":  12,
    "Fasteners":  15,
    "Furnishings": 4,
    "Labels":     10,
    "Machines":    1,
    "Paper":      20,
    "Phones":      1,
    "Storage":     3,
    "Supplies":    5,
    "Tables":      1,
}


# =============================================================================
# 1.  LOAD
# =============================================================================
def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    """
    Read the Superstore CSV and return a raw DataFrame.
    Raises a clear FileNotFoundError if the file is missing.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Dataset not found at: {path}\n"
            "Make sure superstore.csv is inside the data/ folder."
        )
    df = pd.read_csv(path, encoding="latin-1")
    return df


# =============================================================================
# 2.  CLEAN & PREPROCESS
# =============================================================================
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw DataFrame and engineer new columns.

    Steps:
        1. Normalise column names  → lowercase snake_case
        2. Parse date columns      → datetime objects
        3. Remove duplicate rows
        4. Drop rows with missing or zero Sales
        5. Fill remaining string NaNs with "Unknown"
        6. Cast Sales to float safely
        7. Engineer: profit, quantity
        8. Engineer: year, month, month_name, year_month
    """

    df = df.copy()

    # ── 1. Normalise column names ─────────────────────────────────
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    # ── 2. Parse dates (DD/MM/YYYY format in this dataset) ────────
    for col in ["order_date", "ship_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")

    # ── 3. Remove exact duplicate rows ───────────────────────────
    df = df.drop_duplicates()

    # ── 4. Drop rows with no usable Sales value ───────────────────
    df = df.dropna(subset=["sales"])
    df["sales"] = pd.to_numeric(df["sales"], errors="coerce").fillna(0)
    df = df[df["sales"] > 0].reset_index(drop=True)

    # ── 5. Fill remaining NaNs in text columns ────────────────────
    string_cols = df.select_dtypes(include="object").columns
    df[string_cols] = df[string_cols].fillna("Unknown")

    # ── 6. Ensure category column exists (safety) ────────────────
    if "category" not in df.columns:
        df["category"] = "Unknown"
    if "sub_category" not in df.columns:
        df["sub_category"] = "Unknown"

    # ── 7a. Engineer: Profit ──────────────────────────────────────
    #   profit = sales × margin_rate for that row's category
    df["profit"] = df.apply(
        lambda row: round(
            row["sales"] * CATEGORY_MARGINS.get(row["category"], 0.10), 2
        ),
        axis=1,
    )

    # ── 7b. Engineer: Quantity ────────────────────────────────────
    #   Look up average units per sub-category; default = 3
    df["quantity"] = (
        df["sub_category"]
        .map(SUB_CATEGORY_QUANTITY)
        .fillna(3)
        .astype(int)
    )

    # ── 8. Time features from order_date ─────────────────────────
    if "order_date" in df.columns:
        df["year"]       = df["order_date"].dt.year.astype("Int64")
        df["month"]      = df["order_date"].dt.month.astype("Int64")
        df["month_name"] = df["order_date"].dt.strftime("%b")
        df["year_month"] = df["order_date"].dt.to_period("M").astype(str)

    return df


# =============================================================================
# 3.  KPI CALCULATIONS
# =============================================================================
def calculate_kpis(df: pd.DataFrame) -> dict:
    """
    Compute the six headline KPIs from the (possibly filtered) DataFrame.
    Returns safe zeros if the DataFrame is empty.

    Returns dict with keys:
        total_sales, total_profit, total_orders,
        total_quantity, avg_order_value, profit_margin
    """
    if df.empty:
        return {
            "total_sales":     0,
            "total_profit":    0,
            "total_orders":    0,
            "total_quantity":  0,
            "avg_order_value": 0,
            "profit_margin":   0,
        }

    total_sales    = float(df["sales"].sum())
    total_profit   = float(df["profit"].sum())
    total_orders   = int(df["order_id"].nunique())
    total_quantity = int(df["quantity"].sum())
    avg_order_val  = total_sales / total_orders if total_orders > 0 else 0
    profit_margin  = (total_profit / total_sales * 100) if total_sales > 0 else 0

    return {
        "total_sales":     round(total_sales,    2),
        "total_profit":    round(total_profit,   2),
        "total_orders":    total_orders,
        "total_quantity":  total_quantity,
        "avg_order_value": round(avg_order_val,  2),
        "profit_margin":   round(profit_margin,  2),
    }


# =============================================================================
# 4.  AGGREGATION FUNCTIONS  (used by charts and AI engine)
# =============================================================================

def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Total Sales and Profit grouped by Category, sorted by Sales desc."""
    if df.empty:
        return pd.DataFrame(columns=["category", "Sales", "Profit"])
    return (
        df.groupby("category", as_index=False)
        .agg(Sales=("sales", "sum"), Profit=("profit", "sum"))
        .sort_values("Sales", ascending=False)
        .reset_index(drop=True)
    )


def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Total Sales and Profit grouped by Region, sorted by Sales desc."""
    if df.empty:
        return pd.DataFrame(columns=["region", "Sales", "Profit"])
    return (
        df.groupby("region", as_index=False)
        .agg(Sales=("sales", "sum"), Profit=("profit", "sum"))
        .sort_values("Sales", ascending=False)
        .reset_index(drop=True)
    )


def sales_by_segment(df: pd.DataFrame) -> pd.DataFrame:
    """Total Sales and Profit grouped by Customer Segment, sorted by Sales desc."""
    if df.empty:
        return pd.DataFrame(columns=["segment", "Sales", "Profit"])
    return (
        df.groupby("segment", as_index=False)
        .agg(Sales=("sales", "sum"), Profit=("profit", "sum"))
        .sort_values("Sales", ascending=False)
        .reset_index(drop=True)
    )


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """
    Monthly Sales and Profit aggregated by year_month string.
    Sorted chronologically so the line chart flows left → right.
    """
    if df.empty or "year_month" not in df.columns:
        return pd.DataFrame(columns=["year_month", "Sales", "Profit"])
    return (
        df.groupby("year_month", as_index=False)
        .agg(Sales=("sales", "sum"), Profit=("profit", "sum"))
        .sort_values("year_month")
        .reset_index(drop=True)
    )


def yearly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Annual Sales and Profit, sorted by year ascending."""
    if df.empty or "year" not in df.columns:
        return pd.DataFrame(columns=["year", "Sales", "Profit"])
    return (
        df.groupby("year", as_index=False)
        .agg(Sales=("sales", "sum"), Profit=("profit", "sum"))
        .sort_values("year")
        .reset_index(drop=True)
    )


def top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Top-N products ranked by total Sales."""
    if df.empty:
        return pd.DataFrame(columns=["product_name", "Sales", "Profit"])
    return (
        df.groupby("product_name", as_index=False)
        .agg(Sales=("sales", "sum"), Profit=("profit", "sum"))
        .sort_values("Sales", ascending=False)
        .head(n)
        .reset_index(drop=True)
    )


def bottom_profit_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Bottom-N products by estimated Profit (lowest / most at-risk)."""
    if df.empty:
        return pd.DataFrame(columns=["product_name", "Sales", "Profit"])
    return (
        df.groupby("product_name", as_index=False)
        .agg(Sales=("sales", "sum"), Profit=("profit", "sum"))
        .sort_values("Profit", ascending=True)
        .head(n)
        .reset_index(drop=True)
    )


def sales_by_sub_category(df: pd.DataFrame) -> pd.DataFrame:
    """Total Sales and Profit grouped by Sub-Category, sorted by Sales desc."""
    if df.empty:
        return pd.DataFrame(columns=["sub_category", "Sales", "Profit"])
    return (
        df.groupby("sub_category", as_index=False)
        .agg(Sales=("sales", "sum"), Profit=("profit", "sum"))
        .sort_values("Sales", ascending=False)
        .reset_index(drop=True)
    )


def sales_vs_profit_scatter(df: pd.DataFrame) -> pd.DataFrame:
    """
    Per-order Sales vs Profit with Category label.
    Used for the scatter plot visualisation.
    """
    if df.empty:
        return pd.DataFrame(columns=["order_id", "category", "Sales", "Profit"])
    return (
        df.groupby(["order_id", "category"], as_index=False)
        .agg(Sales=("sales", "sum"), Profit=("profit", "sum"))
        .reset_index(drop=True)
    )


# =============================================================================
# 5.  FILTER HELPERS
# =============================================================================

def get_filter_options(df: pd.DataFrame) -> dict:
    """
    Return sorted lists of unique values for every sidebar filter widget.
    Safe — returns empty lists if the column is missing.
    """
    def unique_sorted(col):
        if col not in df.columns:
            return []
        return sorted(df[col].dropna().unique().tolist())

    years = []
    if "year" in df.columns:
        years = sorted(df["year"].dropna().astype(int).unique().tolist())

    return {
        "categories": unique_sorted("category"),
        "regions":    unique_sorted("region"),
        "segments":   unique_sorted("segment"),
        "years":      years,
    }


def apply_filters(
    df: pd.DataFrame,
    categories: list,
    regions: list,
    segments: list,
    years: list,
) -> pd.DataFrame:
    """
    Filter the DataFrame by the selections from the sidebar widgets.

    Rules:
        - An empty list for a filter means "no restriction" (show all).
        - Returning an empty DataFrame is valid — the dashboard handles it.
    """
    filtered = df.copy()

    if categories:
        filtered = filtered[filtered["category"].isin(categories)]
    if regions:
        filtered = filtered[filtered["region"].isin(regions)]
    if segments:
        filtered = filtered[filtered["segment"].isin(segments)]
    if years and "year" in filtered.columns:
        filtered = filtered[filtered["year"].isin(years)]

    return filtered.reset_index(drop=True)
