# =============================================================================
# ai_insights.py
# =============================================================================
# AI-powered Business Insights engine.
#
# HOW IT WORKS (no external API needed):
#   1. Calls the aggregation functions from data_analysis.py to get real numbers.
#   2. Applies business-logic rules to those numbers.
#   3. Writes clear, plain-English sentences based on the results.
#
# This approach is:
#   - 100% offline  (no OpenAI / Gemini key required)
#   - Fully data-driven  (every sentence traces to a real calculation)
#   - Deterministic  (same data → same insight every time)
#
# QUESTION ROUTING:
#   answer_question(question, df) tokenises the user's text, matches keywords
#   to the right insight function, and returns its Markdown output.
# =============================================================================

import pandas as pd

from data_analysis import (
    calculate_kpis,
    sales_by_category,
    sales_by_region,
    sales_by_segment,
    top_products,
    bottom_profit_products,
    yearly_trend,
)


# =============================================================================
# INTERNAL HELPERS
# =============================================================================

def _currency(value: float) -> str:
    """Format a number as a compact, human-readable dollar string."""
    value = float(value)
    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:.2f}"


def _pct(part: float, whole: float) -> str:
    """Return part/whole as a percentage string."""
    if whole == 0:
        return "0.0%"
    return f"{(part / whole * 100):.1f}%"


# =============================================================================
# INSIGHT FUNCTIONS
# Each function receives a (possibly filtered) DataFrame and returns Markdown.
# =============================================================================

def insight_overview(df: pd.DataFrame) -> str:
    """
    High-level business snapshot:
    total sales, profit, orders, AOV, margin — with a health verdict.
    """
    kpis = calculate_kpis(df)

    if kpis["total_orders"] == 0:
        return "No data available for the selected filters. Please widen your selection."

    lines = [
        "## Business Overview",
        "",
        f"The selected data contains **{kpis['total_orders']:,} unique orders** "
        f"with **{_currency(kpis['total_sales'])} in total revenue** and an estimated "
        f"profit of **{_currency(kpis['total_profit'])}**.",
        "",
        f"- Average Order Value : **{_currency(kpis['avg_order_value'])}**",
        f"- Profit Margin       : **{kpis['profit_margin']:.1f}%**",
        f"- Total Items Sold    : **{kpis['total_quantity']:,}**",
        "",
    ]

    # Health assessment based on profit margin
    m = kpis["profit_margin"]
    if m >= 15:
        lines.append(
            "**Profitability: Healthy** — margin exceeds 15%. "
            "The business is generating strong returns."
        )
    elif m >= 10:
        lines.append(
            "**Profitability: Moderate** — margin is between 10–15%. "
            "There is meaningful room to improve through cost optimisation."
        )
    else:
        lines.append(
            "**Profitability: Needs Attention** — margin is below 10%. "
            "Review pricing strategy and cost structure urgently."
        )

    return "\n".join(lines)


def insight_category(df: pd.DataFrame) -> str:
    """
    Per-category revenue, profit, and margin breakdown.
    Identifies the top revenue earner and the lowest-margin category.
    """
    cat_df = sales_by_category(df)

    if cat_df.empty:
        return "No category data available for the current filters."

    total_sales = cat_df["Sales"].sum()
    lines = ["## Category Performance", ""]

    for _, row in cat_df.iterrows():
        share  = _pct(row["Sales"], total_sales)
        margin = (row["Profit"] / row["Sales"] * 100) if row["Sales"] > 0 else 0
        lines.append(
            f"- **{row['category']}** — "
            f"Revenue: {_currency(row['Sales'])} ({share} of total) | "
            f"Estimated Margin: {margin:.1f}%"
        )

    # Best revenue category
    best = cat_df.iloc[0]
    lines += [
        "",
        f"**Top Revenue Category: {best['category']}** "
        f"with {_currency(best['Sales'])} in sales.",
    ]

    # Lowest-margin category (excluding zero-sales rows)
    valid = cat_df[cat_df["Sales"] > 0].copy()
    valid["margin"] = valid["Profit"] / valid["Sales"]
    worst_row = valid.loc[valid["margin"].idxmin()]
    lines.append(
        f"**Lowest Margin Category: {worst_row['category']}** "
        f"at {worst_row['margin'] * 100:.1f}% — "
        "review supplier costs or adjust pricing to improve returns."
    )

    return "\n".join(lines)


def insight_region(df: pd.DataFrame) -> str:
    """
    Revenue and margin by sales region.
    Flags the strongest and weakest region.
    """
    reg_df = sales_by_region(df)

    if reg_df.empty:
        return "No regional data available for the current filters."

    total_sales = reg_df["Sales"].sum()
    lines = ["## Regional Performance", ""]

    for _, row in reg_df.iterrows():
        share  = _pct(row["Sales"], total_sales)
        margin = (row["Profit"] / row["Sales"] * 100) if row["Sales"] > 0 else 0
        lines.append(
            f"- **{row['region']}** — "
            f"{_currency(row['Sales'])} ({share}) | Margin: {margin:.1f}%"
        )

    best_region   = reg_df.iloc[0]["region"]
    worst_region  = reg_df.iloc[-1]["region"]

    lines += [
        "",
        f"**Strongest Region: {best_region}** — leads in total revenue contribution.",
        f"**Weakest Region: {worst_region}** — targeted campaigns or improved "
        "distribution could unlock growth in this area.",
    ]

    return "\n".join(lines)


def insight_trends(df: pd.DataFrame) -> str:
    """
    Year-over-year revenue analysis.
    Calculates total growth from first to last available year.
    """
    yr_df = yearly_trend(df)

    if yr_df.empty or len(yr_df) < 2:
        return (
            "Not enough yearly data to detect trends. "
            "Try widening the Year filter."
        )

    lines = ["## Sales Trends (Year over Year)", ""]

    for _, row in yr_df.iterrows():
        lines.append(f"- **{int(row['year'])}** — {_currency(row['Sales'])}")

    first_sales = float(yr_df.iloc[0]["Sales"])
    last_sales  = float(yr_df.iloc[-1]["Sales"])
    first_year  = int(yr_df.iloc[0]["year"])
    last_year   = int(yr_df.iloc[-1]["year"])

    if first_sales > 0:
        growth     = (last_sales - first_sales) / first_sales * 100
        direction  = "grown" if growth >= 0 else "declined"
        arrow      = "📈" if growth >= 0 else "📉"

        lines += [
            "",
            f"{arrow} Revenue has **{direction} by {abs(growth):.1f}%** "
            f"from {first_year} to {last_year}.",
        ]

        if growth > 20:
            lines.append(
                "Strong growth trajectory — the business is scaling well. "
                "Continue investing in top-performing categories and regions."
            )
        elif growth > 0:
            lines.append(
                "Moderate growth — explore new product lines or untapped "
                "markets to accelerate revenue."
            )
        else:
            lines.append(
                "Revenue has declined — investigate customer churn, "
                "competitive pressure, or demand shifts."
            )

    return "\n".join(lines)


def insight_products(df: pd.DataFrame) -> str:
    """
    Highlights the top 5 best-selling products and the 5 products
    with the lowest estimated profit.
    """
    top_df    = top_products(df, n=5)
    bottom_df = bottom_profit_products(df, n=5)

    if top_df.empty:
        return "No product data available for the current filters."

    lines = ["## Product Insights", ""]

    # Top sellers
    lines.append("**Top 5 Products by Revenue:**")
    for i, (_, row) in enumerate(top_df.iterrows(), start=1):
        name = (row["product_name"][:55] + "…") if len(row["product_name"]) > 55 else row["product_name"]
        lines.append(f"  {i}. {name} — {_currency(row['Sales'])}")

    lines.append("")

    # Lowest profit
    lines.append("**5 Products with Lowest Estimated Profit:**")
    for i, (_, row) in enumerate(bottom_df.iterrows(), start=1):
        name = (row["product_name"][:55] + "…") if len(row["product_name"]) > 55 else row["product_name"]
        lines.append(f"  {i}. {name} — Profit: {_currency(row['Profit'])}")

    lines += [
        "",
        "**Recommendation:** Review low-profit products. Options include "
        "repricing, bundling with high-margin items, or discontinuation.",
    ]

    return "\n".join(lines)


def insight_segment(df: pd.DataFrame) -> str:
    """
    Revenue share by customer segment (Consumer, Corporate, Home Office).
    """
    seg_df = sales_by_segment(df)

    if seg_df.empty:
        return "No segment data available for the current filters."

    total_sales = seg_df["Sales"].sum()
    lines = ["## Customer Segment Analysis", ""]

    for _, row in seg_df.iterrows():
        share = _pct(row["Sales"], total_sales)
        lines.append(f"- **{row['segment']}** — {_currency(row['Sales'])} ({share})")

    best_seg = seg_df.iloc[0]["segment"]
    lines += [
        "",
        f"**Top Segment: {best_seg}** — "
        "prioritise loyalty programmes and upselling strategies here.",
        "Consider segment-specific campaigns: bulk discounts for Corporate, "
        "convenience bundles for Home Office, and loyalty rewards for Consumer.",
    ]

    return "\n".join(lines)


def insight_recommendations(df: pd.DataFrame) -> str:
    """
    Generates 3–6 prioritised strategic recommendations
    derived directly from the calculated KPIs and aggregations.
    """
    kpis   = calculate_kpis(df)
    cat_df = sales_by_category(df)
    reg_df = sales_by_region(df)

    if kpis["total_orders"] == 0:
        return "No data available. Please adjust the sidebar filters."

    lines = ["## Strategic Business Recommendations", ""]
    n = 1   # recommendation counter

    # 1. Margin improvement
    if kpis["profit_margin"] < 12:
        lines.append(
            f"**{n}. Improve Profit Margins** — "
            f"Current margin is {kpis['profit_margin']:.1f}%. "
            "Audit supplier contracts, reduce operational overhead, "
            "and tighten discount policies to push margin above 15%."
        )
        n += 1

    # 2. Low-margin category fix
    if not cat_df.empty:
        valid = cat_df[cat_df["Sales"] > 0].copy()
        valid["margin"] = valid["Profit"] / valid["Sales"]
        low = valid[valid["margin"] < 0.08]
        if not low.empty:
            cat_names = ", ".join(low["category"].tolist())
            lines.append(
                f"**{n}. Fix Low-Margin Categories ({cat_names})** — "
                "These categories return less than 8% estimated profit. "
                "Renegotiate supplier pricing or apply selective price increases."
            )
            n += 1

    # 3. Double down on best category
    if not cat_df.empty:
        top_cat = cat_df.iloc[0]["category"]
        lines.append(
            f"**{n}. Expand the {top_cat} Portfolio** — "
            "This is your highest-revenue category. "
            "Invest in a wider product range and run targeted promotions "
            "to capture greater market share."
        )
        n += 1

    # 4. Grow weak region
    if not reg_df.empty and len(reg_df) > 1:
        weak_region = reg_df.iloc[-1]["region"]
        lines.append(
            f"**{n}. Grow the {weak_region} Region** — "
            "This region generates the least revenue. "
            "Targeted advertising, region-specific deals, or new "
            "distribution partnerships could unlock meaningful growth."
        )
        n += 1

    # 5. Raise average order value
    if kpis["avg_order_value"] < 250:
        lines.append(
            f"**{n}. Increase Average Order Value** — "
            f"Current AOV is {_currency(kpis['avg_order_value'])}. "
            "Implement upselling, cross-selling, and free-shipping "
            "thresholds to drive larger basket sizes."
        )
        n += 1

    # 6. Always-on data culture
    lines.append(
        f"**{n}. Track KPIs Monthly** — "
        "Set clear targets for sales growth, profit margin, and regional "
        "performance. Review progress every month and adjust strategy quickly."
    )

    return "\n".join(lines)


# =============================================================================
# QUESTION ROUTER
# =============================================================================

# Maps keyword lists to insight functions.
# ORDER MATTERS — place more specific keywords before broad ones.
_ROUTES = [
    (["recommend", "suggestion", "strategy", "action", "improve", "advice"],   insight_recommendations),
    (["trend", "growth", "year", "annual", "time", "over time", "history"],     insight_trends),
    (["categor"],                                                                 insight_category),
    (["region", "geographic", "location", "area", "where"],                      insight_region),
    (["product", "item", "sku", "low profit", "best sell", "worst"],             insight_products),
    (["segment", "customer", "consumer", "corporate", "home office"],            insight_segment),
    (["overview", "summary", "overall", "general", "main", "business", "how"],  insight_overview),
]


def answer_question(question: str, df: pd.DataFrame) -> str:
    """
    Route a free-text question to the best matching insight function.

    Matching rules:
        - Lower-case the question and scan for keywords.
        - First match wins (so more-specific routes come first in _ROUTES).
        - If no keyword matches, return the full 7-section report.

    Parameters:
        question : str         — user's question from the text input
        df       : DataFrame   — the currently filtered dataset

    Returns:
        str — Markdown-formatted insight text
    """
    q = question.lower().strip()

    for keywords, func in _ROUTES:
        if any(kw in q for kw in keywords):
            return func(df)

    # No keyword matched — return a comprehensive report
    return generate_full_report(df)


def generate_full_report(df: pd.DataFrame) -> str:
    """
    Build a complete, multi-section business intelligence report
    from the currently filtered dataset.
    Called by the 'Full Report' button in the dashboard.
    """
    separator = "\n\n---\n\n"
    sections = [
        insight_overview(df),
        insight_trends(df),
        insight_category(df),
        insight_region(df),
        insight_segment(df),
        insight_products(df),
        insight_recommendations(df),
    ]
    return separator.join(sections)
