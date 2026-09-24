# AI-Powered E-Commerce Sales Analytics & Business Intelligence System

> A beginner-friendly, fully interactive Streamlit dashboard that analyses the Superstore
> Sales dataset and provides data-driven KPIs, interactive charts, and AI-generated
> business insights — all running locally with no external API required.

---

## 📋 Project Overview

This project demonstrates how to build a complete **Business Intelligence (BI) system** using
Python. It loads the Superstore E-Commerce dataset, cleans and processes the data, calculates
important Key Performance Indicators (KPIs), renders interactive charts with Plotly, and delivers
AI-powered natural-language business insights — all through a professional Streamlit web dashboard.

---

## ✨ Features

| Feature | Description |
|---|---|
| **KPI Dashboard** | Total Sales, Total Orders, Estimated Profit, Profit Margin, AOV, Items Sold |
| **Interactive Charts** | Sales/Profit by Category, Region, Sub-Category, Monthly Trend, Scatter Plot |
| **Product Analysis** | Top 10 products by revenue + 10 lowest-profit products |
| **Sidebar Filters** | Filter by Category, Region, Segment, and Year — all charts update instantly |
| **AI Business Assistant** | Ask natural-language questions; get data-driven insights & recommendations |
| **Full Report Generator** | One-click full business intelligence report from the filtered data |
| **Data Table Viewer** | Browse the filtered dataset directly in the app |

---

## 📂 Dataset Description

**File:** `data/superstore.csv`  
**Source:** Superstore Sales Dataset (Kaggle)  
**Rows:** ~9,800 order line items  
**Columns:**

| Column | Description |
|---|---|
| Row ID | Unique row identifier |
| Order ID | Order identifier (multiple rows per order) |
| Order Date | Date the order was placed (DD/MM/YYYY) |
| Ship Date | Date the order was shipped |
| Ship Mode | Shipping method (Standard Class, Second Class, etc.) |
| Customer ID / Name | Customer identifier and name |
| Segment | Customer segment (Consumer, Corporate, Home Office) |
| Country / City / State / Postal Code | Geographic data |
| Region | Sales region (East, West, Central, South) |
| Product ID / Name | Product identifier and full name |
| Category | Product category (Technology, Furniture, Office Supplies) |
| Sub-Category | Product sub-category (17 sub-categories) |
| Sales | Order line sales amount in USD |

> **Note:** The dataset contains only Sales values. Profit and Quantity are engineered
> using industry-standard category margin assumptions (Technology 18%, Office Supplies 14%,
> Furniture 6%) and typical sub-category order quantities.

---

## 🛠️ Technologies Used

- **Python 3.9+** — Core programming language
- **Streamlit** — Interactive web dashboard framework
- **Pandas** — Data loading, cleaning, and aggregation
- **NumPy** — Numerical computations
- **Plotly Express / Graph Objects** — Interactive visualisations

---

## 📁 Folder Structure

```
AI-Ecommerce-Analytics/
│
├── data/
│   └── superstore.csv          # Superstore sales dataset
│
├── app.py                      # Main Streamlit application
├── data_analysis.py            # Data loading, cleaning, KPIs, aggregations
├── ai_insights.py              # AI-powered insight generation engine
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── PROJECT_REPORT.md           # Full college-level project report
└── .gitignore                  # Git ignore rules
```

---

## ⚙️ System Requirements

- Python **3.9 or higher**
- pip (Python package manager)
- ~100 MB free disk space
- Internet connection only required for first-time package installation

---

## 🚀 Installation & Setup

### Step 1 — Clone or download the project

```bash
# If you have Git:
git clone <your-repo-url>
cd AI-Ecommerce-Analytics

# Or simply download and unzip the project folder.
```

### Step 2 — (Recommended) Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Verify dataset

Make sure `data/superstore.csv` exists inside the project folder.

---

## ▶️ How to Run

```bash
streamlit run app.py
```

Streamlit will automatically open your browser at **http://localhost:8501**.

---

## 🖥️ Usage Instructions

1. **Sidebar Filters** — Use the multiselect dropdowns on the left to filter by Category,
   Region, Customer Segment, and Year. All charts and KPIs update automatically.

2. **Overview & KPIs tab** — View the six headline KPI cards and the main charts
   (category bar, region pie, monthly trend, yearly comparison, segment bar).

3. **Charts tab** — Explore deeper visuals: profit by category, sub-category breakdown,
   sales vs. profit scatter plot, and margin comparison.

4. **Products tab** — See the top 10 best-selling products and the 10 products with the
   lowest estimated profit. Browse the raw filtered data table.

5. **AI Insights tab** — Click a quick-question button or type your own question.
   Hit **Get Insights** for a targeted answer or **Full Report** for a complete
   AI-generated business intelligence report.

---

## 💡 Example Questions for the AI Assistant

- *What are the main business trends?*
- *Which category performs best?*
- *Which region has the highest sales?*
- *Which products have low profit?*
- *Give me business recommendations based on the data.*
- *Show customer segment analysis.*

---

## 📝 Notes for Beginners

- The project uses **no external AI API** — all insights are computed from the data itself.
- Each Python file is heavily commented to help you understand what every section does.
- The `data_analysis.py` module is completely independent — you can import and use its
  functions in a Jupyter notebook as well.
- If you add more columns to the dataset (e.g., real Profit values), you can update
  `data_analysis.py` to use them directly.

---

## 📄 License

This project is for educational purposes. The Superstore dataset is publicly available
on Kaggle under its respective license.
