# Bluestock Mutual Fund Capstone Project

## Project Overview
This project analyzes Indian Mutual Fund data to provide insights into fund performance, investor behavior, and market trends.

## Project Structure
```
bluestock_mf_capstone/
├── data/
│   ├── raw/              # Raw CSV files
│   ├── processed/        # Processed data
│   └── db/              # Database files
├── scripts/             # Python scripts for ETL and analysis
├── notebooks/           # Jupyter notebooks
├── sql/                 # SQL queries
├── dashboard/           # Dashboard files
└── reports/             # Generated reports
```

## Datasets
1. **01_fund_master.csv** - Fund metadata and information
2. **02_nav_history.csv** - Net Asset Value history
3. **03_aum_by_fund_house.csv** - Assets Under Management by fund house
4. **04_monthly_sip_inflows.csv** - Monthly SIP inflows data
5. **05_category_inflows.csv** - Category-wise inflows
6. **06_industry_folio_count.csv** - Industry portfolio holdings count
7. **07_scheme_performance.csv** - Scheme performance metrics
8. **08_investor_transactions.csv** - Investor transaction data
9. **09_portfolio_holdings.csv** - Portfolio holdings details
10. **10_benchmark_indices.csv** - Benchmark indices data

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Place Data Files**
   - Copy all CSV files to `data/raw/` folder

3. **Run Data Ingestion**
   ```bash
   python scripts/data_ingestion.py
   ```

4. **Fetch Live NAV**
   ```bash
   python scripts/live_nav_fetch.py
   ```

## DAY 1 Completion Status
- ✅ Project folder structure created
- ✅ Git repository initialized
- ✅ Data ingestion script prepared
- ✅ Live NAV fetch script prepared
- ✅ Requirements file configured

## Author
Capstone Project - Bluestock

## Date
June 2, 2026
