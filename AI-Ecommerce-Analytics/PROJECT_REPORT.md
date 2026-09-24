# PROJECT REPORT

---

## AI-Powered E-Commerce Sales Analytics & Business Intelligence System

**Submitted by:** [Your Name]  
**Course:** [Your Course Name]  
**Institution:** [Your Institution Name]  
**Academic Year:** 2024–2025  
**Supervisor:** [Supervisor Name]  

---

## Table of Contents

1. Abstract
2. Introduction
3. Problem Statement
4. Objectives
5. Dataset Description
6. Technologies Used
7. System Requirements
8. Methodology
9. Data Cleaning and Preprocessing
10. Exploratory Data Analysis
11. Dashboard Description
12. AI Component
13. Results and Findings
14. Advantages
15. Limitations
16. Future Scope
17. Conclusion
18. References

---

## 1. Abstract

This project presents the design and development of an **AI-Powered E-Commerce Sales Analytics
and Business Intelligence System** built entirely in Python. The system ingests the Superstore
Sales dataset, performs data cleaning and preprocessing using Pandas and NumPy, computes
essential Key Performance Indicators (KPIs), and renders interactive visualisations with
Plotly — all presented through a professional Streamlit web dashboard.

A core feature of the system is an **AI Business Insights Engine** that analyses the computed
metrics and generates natural-language business intelligence reports and strategic
recommendations without requiring any external AI API. Users can ask free-text questions
such as "Which category performs best?" or "Give me business recommendations" and receive
data-driven, contextual answers instantly.

The project demonstrates how modern Python libraries can be combined to build a production-grade
BI tool that is simple enough for a beginner to understand, extend, and deploy locally.

---

## 2. Introduction

The rapid growth of e-commerce has generated enormous volumes of transactional data. Businesses
that can extract meaningful insights from this data gain a significant competitive advantage.
However, traditional analytics tools are often expensive, complex, and inaccessible to small
and medium-sized businesses or students learning data analysis.

This project addresses that gap by building a **free, open-source, locally-runnable analytics
dashboard** using popular Python libraries. The Superstore Sales dataset — a widely-used
public dataset representing a fictional US-based retail company — serves as the foundation
for all analysis.

By combining data engineering, statistical analysis, interactive visualisation, and
rule-based AI, the system demonstrates the full pipeline of a modern BI application:

```
Raw Data → Cleaning → Feature Engineering → KPI Calculation
    → Visualisation → AI Insights → Business Decisions
```

---

## 3. Problem Statement

Retail and e-commerce businesses collect large amounts of sales data but often lack the tools
or expertise to convert that data into actionable business intelligence. Key challenges include:

- **Data Quality Issues:** Raw sales data contains missing values, incorrect formats, and
  duplicate records that distort analysis.
- **KPI Visibility Gap:** Decision-makers cannot quickly see which products, categories, or
  regions are performing well or poorly.
- **Insight Accessibility:** Traditional BI tools (Tableau, Power BI) require licences and
  training. Python-based alternatives are often too technical for business users.
- **Absence of Recommendations:** Dashboards typically show *what* is happening but not
  *why* or *what to do about it*.

This project solves all four challenges in a single, beginner-accessible application.

---

## 4. Objectives

The primary objectives of this project are:

1. **Data Pipeline:** Load, clean, and preprocess the Superstore dataset for reliable analysis.
2. **Feature Engineering:** Derive estimated Profit and Quantity features from the available
   Sales data using industry-standard margin assumptions.
3. **KPI Calculation:** Compute Total Sales, Total Orders, Estimated Profit, Profit Margin,
   Average Order Value, and Items Sold dynamically from filtered data.
4. **Interactive Visualisation:** Build at least eight interactive Plotly charts covering
   categories, regions, trends, products, and profitability.
5. **Filtering:** Allow users to slice data by Category, Region, Customer Segment, and Year
   with instant chart updates.
6. **AI Insights:** Generate natural-language business insights and strategic recommendations
   from the analysed data without an external API.
7. **Accessibility:** Keep the codebase clean, commented, and understandable for beginners.

---

## 5. Dataset Description

### Source
The Superstore Sales dataset is publicly available on Kaggle and represents transactional
sales records of a fictional US-based retail store.

### File Details
| Property | Value |
|---|---|
| File name | superstore.csv |
| Format | CSV (Comma-Separated Values) |
| Encoding | Latin-1 |
| Total records | ~9,800 rows |
| Date format | DD/MM/YYYY |

### Column Reference

| Column | Data Type | Description |
|---|---|---|
| Row ID | Integer | Sequential unique row number |
| Order ID | String | Order identifier (multiple lines per order) |
| Order Date | Date | Date the order was placed |
| Ship Date | Date | Date the order was shipped |
| Ship Mode | String | Shipping class (Standard, Second, First, Same Day) |
| Customer ID | String | Unique customer identifier |
| Customer Name | String | Full customer name |
| Segment | String | Customer segment: Consumer, Corporate, Home Office |
| Country | String | Always "United States" |
| City | String | Delivery city |
| State | String | Delivery state |
| Postal Code | Integer | Postal/ZIP code |
| Region | String | Sales region: East, West, Central, South |
| Product ID | String | Unique product SKU |
| Category | String | Product category: Furniture, Office Supplies, Technology |
| Sub-Category | String | 17 sub-categories (Chairs, Phones, Binders, etc.) |
| Product Name | String | Full product description |
| Sales | Float | Order line revenue in USD |

### Engineered Columns (added during preprocessing)

| Column | Description |
|---|---|
| profit | Estimated profit = Sales × category margin rate |
| quantity | Estimated units per order line (by sub-category) |
| year | Extracted from Order Date |
| month | Extracted from Order Date |
| month_name | Abbreviated month name |
| year_month | Period string (e.g., "2017-01") for time-series plots |

### Margin Assumptions
Since the source dataset contains only Sales values (no Profit column), profit is estimated
using industry-standard retail margin rates:

| Category | Margin Rate |
|---|---|
| Technology | 18% |
| Office Supplies | 14% |
| Furniture | 6% |

---

## 6. Technologies Used

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.9+ | Core programming language |
| Streamlit | ≥ 1.32 | Web dashboard framework |
| Pandas | ≥ 2.0 | Data loading, cleaning, aggregation |
| NumPy | ≥ 1.26 | Numerical operations |
| Plotly Express | ≥ 5.20 | Interactive charts and visualisations |

### Why These Technologies?

- **Streamlit** was chosen because it converts Python scripts into interactive web apps with
  minimal boilerplate — ideal for beginners.
- **Pandas** is the industry-standard library for tabular data manipulation in Python.
- **Plotly** provides production-quality interactive charts that work natively in Streamlit.
- **NumPy** complements Pandas for efficient array operations.
- No external AI API (OpenAI, Gemini, etc.) is used — insights are derived programmatically,
  making the project 100% offline and free to run.

---

## 7. System Requirements

### Minimum Hardware
- CPU: Dual-core 1.5 GHz or faster
- RAM: 4 GB (8 GB recommended for smooth performance)
- Storage: 200 MB free disk space

### Software Requirements
| Software | Version |
|---|---|
| Python | 3.9 or higher |
| pip | Latest version |
| Web Browser | Chrome, Firefox, Edge (any modern browser) |
| OS | Windows 10+, macOS 10.15+, Ubuntu 20.04+ |

---

## 8. Methodology

The project follows a structured data science workflow:

```
1. Data Acquisition        → Load CSV from the data/ folder
2. Data Understanding      → Inspect columns, types, and sample rows
3. Data Cleaning           → Handle nulls, duplicates, date parsing
4. Feature Engineering     → Derive Profit, Quantity, time features
5. Exploratory Analysis    → Aggregations, KPI calculations
6. Visualisation           → Plotly interactive charts in Streamlit
7. AI Insight Generation   → Rule-based NLG from computed metrics
8. Dashboard Integration   → Filters, tabs, responsive layout
```

### Module Architecture

```
app.py
  ├── imports data_analysis.py   (data pipeline)
  └── imports ai_insights.py     (insight engine)
        └── imports data_analysis.py (aggregations)
```

The separation of concerns means:
- `data_analysis.py` can be used independently (e.g., in Jupyter notebooks).
- `ai_insights.py` is a pure analytics layer with no UI dependencies.
- `app.py` is purely a presentation layer — it calls functions, renders results.

---

## 9. Data Cleaning and Preprocessing

The `clean_data()` function in `data_analysis.py` performs the following steps:

### 9.1 Column Renaming
Column names are normalised to lowercase snake_case (e.g., `Order Date` → `order_date`)
to prevent KeyError issues and improve code readability.

### 9.2 Date Parsing
`Order Date` and `Ship Date` are parsed with `dayfirst=True` to handle the DD/MM/YYYY
format used in the dataset. Invalid dates are coerced to `NaT`.

### 9.3 Duplicate Removal
`DataFrame.drop_duplicates()` removes fully identical rows.

### 9.4 Missing Value Handling
- Rows with missing or zero Sales values are dropped (they contribute no revenue).
- Remaining null values in string columns are filled with `"Unknown"`.

### 9.5 Type Enforcement
`Sales` is cast to float using `pd.to_numeric(..., errors='coerce')` to handle any
non-numeric values gracefully.

### 9.6 Feature Engineering
- **Profit:** Calculated as `Sales × margin_rate` per category row.
- **Quantity:** Mapped from a sub-category lookup table of average units per order line.
- **Time Features:** `year`, `month`, `month_name`, and `year_month` extracted from `order_date`.

---

## 10. Exploratory Data Analysis

EDA is performed through the aggregation functions in `data_analysis.py` and visualised
in the dashboard:

### 10.1 Summary Statistics
- Total records: ~9,800 order lines
- Unique orders: ~5,000
- Date range: 2015–2018 (4 years)
- Three product categories, four sales regions, three customer segments

### 10.2 Sales Distribution by Category
Technology generates the highest revenue per order due to high-value items (phones,
copiers, machines). Office Supplies has the highest order volume. Furniture has the
lowest profit margin.

### 10.3 Regional Analysis
The West and East regions consistently outperform Central and South in total revenue.
Regional imbalance suggests untapped market potential in underperforming areas.

### 10.4 Time-Series Analysis
Monthly trend analysis reveals seasonal peaks in Q4 (October–December), consistent
with end-of-year retail patterns. Year-over-year analysis shows positive revenue growth.

### 10.5 Customer Segments
Consumer segment accounts for the largest share of orders, followed by Corporate.
Corporate customers tend to place larger individual orders (higher AOV).

---

## 11. Dashboard Description

The Streamlit dashboard is organised into four tabs:

### Tab 1: Overview & KPIs
- **Six KPI metric cards:** Total Sales, Total Orders, Estimated Profit, Profit Margin,
  Average Order Value, Items Sold
- **Bar chart:** Sales by Category
- **Donut chart:** Revenue Share by Region
- **Line chart:** Monthly Sales Trend
- **Grouped bar chart:** Annual Sales vs Estimated Profit
- **Bar chart:** Sales by Customer Segment

### Tab 2: Charts
- **Bar chart:** Estimated Profit by Category
- **Horizontal bar chart:** Top 15 Sub-Categories (colour = profit)
- **Scatter plot:** Sales vs Estimated Profit per Order (colour = category)
- **Bar charts:** Profit by Region, Profit Margin % by Category

### Tab 3: Products
- **Horizontal bar chart:** Top 10 Products by Revenue
- **Horizontal bar chart:** 10 Products with Lowest Estimated Profit
- **Expandable data table:** Filtered dataset (first 500 rows)

### Tab 4: AI Insights
- Six quick-question buttons for common business questions
- Free-text input for custom questions
- "Get Insights" button for targeted analysis
- "Full Report" button for a comprehensive BI report

### Sidebar Filters
All four filters (Category, Region, Segment, Year) are Streamlit `multiselect` widgets.
Selecting no items in a filter is equivalent to selecting all items. Every chart and KPI
card updates reactively when a filter changes.

---

## 12. AI Component

### Architecture
The AI Insights Engine in `ai_insights.py` uses a **rule-based Natural Language Generation (NLG)**
approach rather than a large language model. This keeps the project:

- **100% offline** — no API keys or internet connection needed at runtime
- **Deterministic** — same data always produces the same insight
- **Explainable** — every sentence traces directly to a calculated metric
- **Fast** — insights generate in milliseconds

### Question Routing
The `answer_question(question, df)` function tokenises the user's question and matches
keywords against a priority-ordered routing table:

| Keywords | Insight Function |
|---|---|
| overview, summary, overall | `insight_overview()` |
| trend, growth, year, annual | `insight_trends()` |
| category | `insight_category()` |
| region, geographic, area | `insight_region()` |
| product, item, low profit | `insight_products()` |
| segment, customer, consumer | `insight_segment()` |
| recommend, strategy, improve | `insight_recommendations()` |

If no keyword matches, a full multi-section report is returned.

### Insight Functions
Each function receives the **filtered** DataFrame and produces contextual Markdown:

- `insight_overview()` — KPI summary with profitability health assessment
- `insight_category()` — Per-category revenue and margin breakdown
- `insight_region()` — Regional revenue share with growth recommendations
- `insight_trends()` — YoY growth rate with directional commentary
- `insight_products()` — Top sellers and loss-maker identification
- `insight_segment()` — Segment revenue share with retention strategies
- `insight_recommendations()` — Prioritised strategic recommendations

---

## 13. Results and Findings

> Note: The following findings are representative of the full unfiltered Superstore dataset.
> Actual numbers will vary based on sidebar filter selections.

### 13.1 Revenue Summary
The Superstore dataset spans four years (2015–2018) with consistent year-over-year
revenue growth. The business demonstrates positive momentum across all categories.

### 13.2 Category Performance
- **Technology** generates the highest revenue per order and the highest profit margin (~18%).
- **Office Supplies** has the highest order count but lower per-order value.
- **Furniture** produces the lowest profit margin (~6%), suggesting high cost of goods.

### 13.3 Regional Performance
- **West** and **East** regions lead in total revenue.
- **Central** and **South** regions show lower performance, representing growth opportunities.

### 13.4 Seasonal Patterns
- Monthly trend analysis confirms Q4 seasonality — sales spike in October, November,
  and December consistent with holiday shopping behaviour.

### 13.5 Customer Segments
- **Consumer** segment accounts for approximately 50% of total orders.
- **Corporate** customers generate higher average order values.
- **Home Office** is the smallest segment but growing year over year.

### 13.6 Product Insights
- High-value Technology items (phones, copiers, machines) dominate the top-10 revenue list.
- Low-profit products are concentrated in Furniture (especially Tables) due to low margins.

---

## 14. Advantages

1. **No Cost:** Entirely open-source; no licences, subscriptions, or API keys required.
2. **Fully Offline:** Runs completely on a local machine with no internet dependency at runtime.
3. **Beginner Friendly:** Each file is well-commented and follows a clear, logical structure.
4. **Extensible:** New charts, KPIs, or insight types can be added by following existing patterns.
5. **Fast:** Streamlit's `@st.cache_data` decorator prevents reloading data on every interaction.
6. **Interactive:** Plotly charts support hover, zoom, pan, and export out of the box.
7. **Filter-Aware AI:** The AI insights engine operates on the filtered dataset, so insights
   are always contextually relevant to the user's current view.
8. **Safe:** All filter and empty-data edge cases are handled to prevent crashes.

---

## 15. Limitations

1. **Estimated Profit:** Since the source dataset lacks a Profit column, profit figures are
   estimated using fixed margin rates and may not reflect actual business performance.
2. **Static Margin Rates:** Category margin assumptions are fixed constants. Real businesses
   have variable margins across products, seasons, and customers.
3. **US-Only Data:** The dataset covers only United States geography, limiting global insights.
4. **No Forecasting:** The current system is descriptive (what happened) not predictive
   (what will happen). No ML forecasting models are included.
5. **Rule-Based AI:** The insight engine uses keyword matching and templates rather than a
   true language model, so it cannot answer arbitrary complex questions.
6. **Single Dataset:** The system is designed for this specific dataset schema. Adapting it
   to a different dataset requires changes to column name references.

---

## 16. Future Scope

1. **Real Profit Data:** Connect to a database or ERP system that provides actual profit
   and cost data.
2. **Predictive Analytics:** Integrate scikit-learn to forecast future sales using time-series
   models (ARIMA, Prophet) or regression.
3. **LLM Integration:** Replace the rule-based insight engine with an OpenAI GPT or
   Google Gemini API call for richer, more conversational responses.
4. **Customer Analytics:** Add customer lifetime value (CLV), churn analysis, and RFM
   (Recency, Frequency, Monetary) segmentation.
5. **Inventory Module:** Incorporate stock level data to identify stockout risks and
   overstock situations.
6. **Export Functionality:** Allow users to export filtered data and charts as PDF reports.
7. **Multi-Dataset Support:** Build a generic data pipeline that adapts to different CSV schemas.
8. **Authentication:** Add user login so different roles (manager, analyst) see different views.
9. **Cloud Deployment:** Deploy to Streamlit Community Cloud, AWS, or Azure for team access.
10. **Automated Alerts:** Email or Slack notifications when KPIs fall below defined thresholds.

---

## 17. Conclusion

This project successfully demonstrates that a complete, professional-grade Business Intelligence
system can be built using only free, open-source Python libraries. By combining Pandas for
data engineering, Plotly for interactive visualisation, and Streamlit for the web interface,
the system delivers a polished analytics dashboard accessible to users with no data science
background.

The AI Business Insights Engine bridges the critical gap between raw data and actionable
decisions by translating computed metrics into clear, concise natural-language recommendations.
Although the engine is rule-based rather than LLM-powered, it is fully data-driven — every
insight it produces is traceable to a real calculation on the actual dataset.

The project achieves all stated objectives: data cleaning, KPI computation, interactive
filtering, multi-chart visualisation, and AI-assisted insights — while remaining simple enough
for a Python beginner to read, run, and extend. It serves as a strong foundation for more
advanced analytics features and real-world BI applications.

---

## 18. References

1. McKinney, W. (2012). *Python for Data Analysis*. O'Reilly Media.
2. Streamlit Documentation. (2024). *Streamlit — A faster way to build and share data apps*.
   https://docs.streamlit.io
3. Plotly Technologies Inc. (2024). *Plotly Python Graphing Library*.
   https://plotly.com/python/
4. Pandas Development Team. (2024). *pandas: powerful Python data analysis toolkit*.
   https://pandas.pydata.org/docs/
5. NumPy Developers. (2024). *NumPy — The fundamental package for scientific computing*.
   https://numpy.org/doc/
6. Kaggle. (2019). *Sample Superstore Dataset*.
   https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
7. Tableau. (2021). *Superstore Sales Analysis — Sample Workbook*. Tableau Software.
8. Han, J., Kamber, M., & Pei, J. (2011). *Data Mining: Concepts and Techniques* (3rd ed.).
   Morgan Kaufmann.
9. Provost, F., & Fawcett, T. (2013). *Data Science for Business*. O'Reilly Media.
10. VanderPlas, J. (2016). *Python Data Science Handbook*. O'Reilly Media.

---

*End of Report*
