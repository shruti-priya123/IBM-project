# =============================================================================
# app.py
# =============================================================================
# Main Streamlit application for the
# "AI-Powered E-Commerce Sales Analytics & Business Intelligence System"
#
# HOW TO RUN:
#     streamlit run app.py
#
# STRUCTURE:
#     Sidebar  — filters (Category, Region, Segment, Year)
#     Tab 1    — Overview & KPIs
#     Tab 2    — Charts
#     Tab 3    — Products
#     Tab 4    — AI Insights
# =============================================================================

import streamlit as st
import plotly.express as px

# Our own modules
from data_analysis import (
    load_data,
    clean_data,
    calculate_kpis,
    sales_by_category,
    sales_by_region,
    sales_by_segment,
    monthly_trend,
    yearly_trend,
    top_products,
    bottom_profit_products,
    sales_by_sub_category,
    sales_vs_profit_scatter,
    get_filter_options,
    apply_filters,
)
from ai_insights import answer_question, generate_full_report


# =============================================================================
# PAGE CONFIG  — must be the very first Streamlit call
# =============================================================================
st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# CUSTOM CSS  — makes the dashboard look clean and professional
# =============================================================================
st.markdown(
    """
    <style>
        /* Light grey page background */
        .main { background-color: #f7f8fa; }

        /* KPI metric cards */
        [data-testid="metric-container"] {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 18px 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }

        /* Dark sidebar */
        [data-testid="stSidebar"] {
            background-color: #1e293b;
        }
        [data-testid="stSidebar"] * {
            color: #f1f5f9 !important;
        }

        /* Tab font size */
        button[data-baseweb="tab"] {
            font-size: 0.95rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# DATA LOADING
# @st.cache_data means Streamlit loads and cleans the CSV only once,
# then reuses the result — makes the app fast on every filter change.
# =============================================================================
@st.cache_data(show_spinner="Loading dataset…")
def get_data():
    raw = load_data()
    return clean_data(raw)


# Load data — show a friendly message if the file is missing
try:
    df_full = get_data()
except FileNotFoundError as err:
    st.error(str(err))
    st.stop()   # halt the app here — nothing else can run without data


# =============================================================================
# SIDEBAR — FILTERS
# =============================================================================
with st.sidebar:
    st.markdown("## 🛒 E-Commerce Analytics")
    st.caption("AI-Powered Business Intelligence")
    st.markdown("---")

    # Get all available unique values from the full (unfiltered) dataset
    options = get_filter_options(df_full)

    st.markdown("### Filters")

    selected_categories = st.multiselect(
        label="Category",
        options=options["categories"],
        default=options["categories"],   # all selected by default
    )

    selected_regions = st.multiselect(
        label="Region",
        options=options["regions"],
        default=options["regions"],
    )

    selected_segments = st.multiselect(
        label="Customer Segment",
        options=options["segments"],
        default=options["segments"],
    )

    selected_years = st.multiselect(
        label="Year",
        options=options["years"],
        default=options["years"],
    )

    st.markdown("---")
    st.caption(f"Dataset: {len(df_full):,} records")
    st.caption("Source: Superstore Sales CSV")


# =============================================================================
# APPLY FILTERS
# =============================================================================
df = apply_filters(
    df_full,
    categories=selected_categories,
    regions=selected_regions,
    segments=selected_segments,
    years=selected_years,
)

# Safety check — show a warning and stop if filters return zero rows
if df.empty:
    st.warning(
        "No records match the current filter selection. "
        "Please select at least one option in each filter."
    )
    st.stop()


# =============================================================================
# PAGE HEADER
# =============================================================================
st.title("📊 AI-Powered E-Commerce Sales Analytics")
st.caption(
    f"Showing **{len(df):,} records** "
    f"| Years: **{', '.join(str(y) for y in sorted(df['year'].dropna().astype(int).unique()))}** "
    f"| Use the sidebar to filter."
)
st.markdown("---")


# =============================================================================
# TABS
# =============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Overview & KPIs",
    "📊 Charts",
    "🛍️ Products",
    "🤖 AI Insights",
])


# ─────────────────────────────────────────────────────────────────
# TAB 1 — OVERVIEW & KPIs
# ─────────────────────────────────────────────────────────────────
with tab1:

    # ── KPI Cards ────────────────────────────────────────────────
    kpis = calculate_kpis(df)

    st.subheader("Key Performance Indicators")

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric(label="Total Sales",         value=f"${kpis['total_sales']:,.0f}")
    col2.metric(label="Total Orders",        value=f"{kpis['total_orders']:,}")
    col3.metric(label="Estimated Profit",    value=f"${kpis['total_profit']:,.0f}")
    col4.metric(label="Profit Margin",       value=f"{kpis['profit_margin']:.1f}%")
    col5.metric(label="Avg Order Value",     value=f"${kpis['avg_order_value']:,.0f}")
    col6.metric(label="Items Sold",          value=f"{kpis['total_quantity']:,}")

    st.markdown("---")

    # ── Row 1: Sales by Category  |  Sales by Region ─────────────
    left, right = st.columns(2)

    with left:
        st.subheader("Sales by Category")
        cat_df = sales_by_category(df)
        if not cat_df.empty:
            fig = px.bar(
                cat_df,
                x="category",
                y="Sales",
                color="category",
                text_auto=".2s",
                color_discrete_sequence=px.colors.qualitative.Set2,
            )
            fig.update_layout(showlegend=False, plot_bgcolor="#ffffff", height=360)
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Revenue Share by Region")
        reg_df = sales_by_region(df)
        if not reg_df.empty:
            fig = px.pie(
                reg_df,
                values="Sales",
                names="region",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            fig.update_layout(height=360)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Row 2: Monthly Sales Trend ────────────────────────────────
    st.subheader("Monthly Sales Trend")
    trend_df = monthly_trend(df)
    if not trend_df.empty:
        fig = px.line(
            trend_df,
            x="year_month",
            y="Sales",
            markers=True,
            color_discrete_sequence=["#3b82f6"],
        )
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Sales ($)",
            plot_bgcolor="#ffffff",
            height=380,
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 3: Yearly Bar  |  Segment Bar ────────────────────────
    left2, right2 = st.columns(2)

    with left2:
        st.subheader("Year-over-Year Sales vs Profit")
        yr_df = yearly_trend(df)
        if not yr_df.empty and len(yr_df) >= 1:
            fig = px.bar(
                yr_df,
                x="year",
                y=["Sales", "Profit"],
                barmode="group",
                color_discrete_sequence=["#3b82f6", "#8b5cf6"],
            )
            fig.update_layout(plot_bgcolor="#ffffff", height=360)
            st.plotly_chart(fig, use_container_width=True)

    with right2:
        st.subheader("Sales by Customer Segment")
        seg_df = sales_by_segment(df)
        if not seg_df.empty:
            fig = px.bar(
                seg_df,
                x="segment",
                y="Sales",
                color="segment",
                text_auto=".2s",
                color_discrete_sequence=px.colors.qualitative.Vivid,
            )
            fig.update_layout(showlegend=False, plot_bgcolor="#ffffff", height=360)
            st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────────
# TAB 2 — CHARTS
# ─────────────────────────────────────────────────────────────────
with tab2:

    # ── Profit by Category ────────────────────────────────────────
    st.subheader("Estimated Profit by Category")
    cat_df = sales_by_category(df)
    if not cat_df.empty:
        fig = px.bar(
            cat_df,
            x="category",
            y="Profit",
            color="category",
            text_auto=".2s",
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig.update_layout(showlegend=False, plot_bgcolor="#ffffff", height=380)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Sub-category horizontal bar ───────────────────────────────
    st.subheader("Sales by Sub-Category (top 15)")
    sub_df = sales_by_sub_category(df)
    if not sub_df.empty:
        fig = px.bar(
            sub_df.head(15),
            x="Sales",
            y="sub_category",
            orientation="h",
            color="Profit",
            color_continuous_scale="Teal",
            text_auto=".2s",
        )
        fig.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            plot_bgcolor="#ffffff",
            height=480,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Scatter: Sales vs Profit ──────────────────────────────────
    st.subheader("Sales vs Estimated Profit — by Order")
    scatter_df = sales_vs_profit_scatter(df)
    if not scatter_df.empty:
        fig = px.scatter(
            scatter_df,
            x="Sales",
            y="Profit",
            color="category",
            size="Sales",
            hover_data=["order_id"],
            opacity=0.6,
            color_discrete_sequence=px.colors.qualitative.Set1,
        )
        fig.update_layout(plot_bgcolor="#ffffff", height=430)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Profit by Region  |  Margin by Category ──────────────────
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Profit by Region")
        reg_df = sales_by_region(df)
        if not reg_df.empty:
            fig = px.bar(
                reg_df,
                x="region",
                y="Profit",
                color="region",
                text_auto=".2s",
                color_discrete_sequence=px.colors.qualitative.Bold,
            )
            fig.update_layout(showlegend=False, plot_bgcolor="#ffffff", height=360)
            st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("Profit Margin % by Category")
        cat_df = sales_by_category(df)
        if not cat_df.empty:
            cat_df = cat_df.copy()
            cat_df["Margin %"] = (cat_df["Profit"] / cat_df["Sales"] * 100).round(2)
            fig = px.bar(
                cat_df,
                x="category",
                y="Margin %",
                color="category",
                text_auto=".1f",
                color_discrete_sequence=px.colors.qualitative.Antique,
            )
            fig.update_layout(showlegend=False, plot_bgcolor="#ffffff", height=360)
            st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────────
# TAB 3 — PRODUCTS
# ─────────────────────────────────────────────────────────────────
with tab3:

    col_top, col_low = st.columns(2)

    # ── Top 10 Products by Sales ──────────────────────────────────
    with col_top:
        st.subheader("Top 10 Products by Revenue")
        top_df = top_products(df, n=10)
        if not top_df.empty:
            # Shorten long names so they fit on the chart axis
            top_df = top_df.copy()
            top_df["name"] = top_df["product_name"].str[:45]
            fig = px.bar(
                top_df,
                x="Sales",
                y="name",
                orientation="h",
                color="Sales",
                color_continuous_scale="Blues",
                text_auto=".2s",
            )
            fig.update_layout(
                yaxis=dict(categoryorder="total ascending"),
                plot_bgcolor="#ffffff",
                height=460,
            )
            st.plotly_chart(fig, use_container_width=True)

    # ── 10 Products with Lowest Profit ───────────────────────────
    with col_low:
        st.subheader("10 Products with Lowest Estimated Profit")
        bot_df = bottom_profit_products(df, n=10)
        if not bot_df.empty:
            bot_df = bot_df.copy()
            bot_df["name"] = bot_df["product_name"].str[:45]
            fig = px.bar(
                bot_df,
                x="Profit",
                y="name",
                orientation="h",
                color="Profit",
                color_continuous_scale="Reds_r",
                text_auto=".2s",
            )
            fig.update_layout(
                yaxis=dict(categoryorder="total descending"),
                plot_bgcolor="#ffffff",
                height=460,
            )
            st.plotly_chart(fig, use_container_width=True)

    # ── Raw Data Table ────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Raw Data (first 500 rows)")
    with st.expander("Click to expand / collapse the data table"):
        show_cols = [
            "order_id", "order_date", "customer_name", "segment",
            "region", "category", "sub_category", "product_name",
            "sales", "profit", "quantity",
        ]
        # Only include columns that actually exist in the DataFrame
        show_cols = [c for c in show_cols if c in df.columns]
        st.dataframe(df[show_cols].head(500), use_container_width=True)


# ─────────────────────────────────────────────────────────────────
# TAB 4 — AI INSIGHTS
# ─────────────────────────────────────────────────────────────────
with tab4:

    st.subheader("AI Business Assistant")
    st.caption(
        "All insights are generated from the actual dataset — no external API needed. "
        "The answers update automatically when you change the sidebar filters."
    )

    # ── Quick-question buttons ────────────────────────────────────
    st.markdown("**Quick Questions — click any button for an instant answer:**")

    QUICK_QUESTIONS = [
        "What are the main business trends?",
        "Which category performs best?",
        "Which region has the highest sales?",
        "Which products have low profit?",
        "Give me business recommendations.",
        "Show customer segment analysis.",
    ]

    # Store the active question between widget interactions
    if "active_question" not in st.session_state:
        st.session_state["active_question"] = ""

    # Render buttons in 3 columns
    btn_cols = st.columns(3)
    for idx, q in enumerate(QUICK_QUESTIONS):
        if btn_cols[idx % 3].button(q, key=f"btn_{idx}", use_container_width=True):
            st.session_state["active_question"] = q

    st.markdown("---")

    # ── Free-text input ───────────────────────────────────────────
    user_q = st.text_input(
        label="Or type your own question:",
        value=st.session_state["active_question"],
        placeholder="e.g.  Which segment should I focus on?",
    )

    # ── Action buttons ────────────────────────────────────────────
    btn_col1, btn_col2, _ = st.columns([1, 1, 3])
    ask_btn    = btn_col1.button("Get Insights", type="primary")
    report_btn = btn_col2.button("Full Report")

    # ── Response area ─────────────────────────────────────────────
    if ask_btn and user_q.strip():
        with st.spinner("Analysing data…"):
            result = answer_question(user_q, df)
        st.markdown(result)

    elif report_btn:
        with st.spinner("Building full report…"):
            result = generate_full_report(df)
        st.markdown(result)

    elif st.session_state["active_question"] and not ask_btn:
        # Auto-answer when a quick-question button was clicked
        with st.spinner("Analysing data…"):
            result = answer_question(st.session_state["active_question"], df)
        st.markdown(result)

    # ── Information note ──────────────────────────────────────────
    st.markdown("---")
    st.info(
        "**How the AI works:** "
        "This assistant calculates real KPIs and aggregations from your "
        "filtered dataset, then converts those numbers into plain-English "
        "insights using business-logic rules. "
        "Profit is estimated using category margin rates: "
        "Technology 18%, Office Supplies 14%, Furniture 6%."
    )


# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#94a3b8; font-size:0.8rem;'>"
    "AI-Powered E-Commerce Sales Analytics &nbsp;|&nbsp; "
    "Built with Streamlit · Plotly · Pandas"
    "</div>",
    unsafe_allow_html=True,
)
