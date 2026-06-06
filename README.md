# Bluestock Mutual Fund Capstone Project

## Project Overview
This project is a Mutual Fund Analytics Platform that ingests, cleans, stores, and analyzes mutual fund datasets to generate business insights and visualizations.

## Project Structure
```
bluestock_mf_capstone/
├── data/
│   ├── raw/              # Raw CSV files
│   ├── processed/        # Cleaned data files
│   └── db/               # SQLite database files
├── notebooks/           # Jupyter notebooks
├── reports/             # Reports and exports
│   └── charts/          # Exported visualization PNGs
├── scripts/             # Supporting scripts
├── sql/                 # Schema and query SQL files
├── dashboard/           # Dashboard or presentation files
├── etl_pipeline.py      # ETL pipeline entrypoint
├── data_dictionary.md   # Dataset definitions and field descriptions
├── README.md            # Project documentation
└── requirements.txt     # Python dependencies
```

## Datasets
1. **01_fund_master.csv** - Fund metadata and AMFI scheme details
2. **02_nav_history.csv** - Daily NAV history for schemes
3. **03_aum_by_fund_house.csv** - Quarterly AUM by AMC
4. **04_monthly_sip_inflows.csv** - Monthly SIP inflow trends
5. **05_category_inflows.csv** - Category-level inflows
6. **06_industry_folio_count.csv** - Folio growth statistics
7. **07_scheme_performance.csv** - Scheme performance and risk metrics
8. **08_investor_transactions.csv** - Investor transaction and demographic data
9. **09_portfolio_holdings.csv** - Portfolio holdings by scheme
10. **10_benchmark_indices.csv** - Benchmark index values

## Day 2 — Data Cleaning & SQL Database Design
1. Copy the source CSV files into `data/raw/`.
2. Run the ETL pipeline:
   ```bash
   python etl_pipeline.py
   ```
3. Cleaned datasets are saved to `data/processed/`.
4. The SQLite database is created at `data/db/bluestock_mf.db`.
5. Schema and analytical queries are available in the `sql/` folder.

## Day 3 — Exploratory Data Analysis
1. Open the EDA notebook:
   ```bash
   jupyter notebook notebooks/EDA_Analysis.ipynb
   ```
2. The notebook generates 15+ visualizations and exports PNG charts to `reports/charts/`.
3. Key analysis topics include NAV trends, AUM growth, SIP inflows, category heatmaps, investor demographics, state-level transactions, fund performance, and benchmark comparisons.

## Day 4 — Fund Performance Analytics
1. Run the performance analytics script:
   ```bash
   python scripts/performance_analytics.py
   ```
2. Or open the Day 4 notebook:
   ```bash
   jupyter notebook notebooks/Performance_Analytics.ipynb
   ```
3. Generated outputs include:
   - `reports/fund_scorecard.csv`
   - `reports/alpha_beta.csv`
   - `reports/benchmark_comparison.csv`
   - `reports/charts/benchmark_comparison_chart.png`

## Day 5 — Dashboard Development
1. Run the dashboard prep script:
   ```bash
   python dashboard/dashboard_data_prep.py
   ```
2. Dashboard-ready CSV files are generated in `dashboard/data/`.
3. Placeholder dashboard screenshots are exported to `reports/dashboard_screenshots/`.
4. Review dashboard documentation in `dashboard/dashboard_summary.md` for page definitions, KPIs, and filter behavior.

## Generated Artifacts
- `etl_pipeline.py`
- `sql/schema.sql`
- `sql/queries.sql`
- `data_dictionary.md`
- `notebooks/EDA_Analysis.ipynb`
- `notebooks/Performance_Analytics.ipynb`
- `dashboard/dashboard_data_prep.py`
- `dashboard/dashboard_summary.md`
- `dashboard/README.md`
- `data/db/bluestock_mf.db`
- `reports/charts/` PNG exports
- `reports/dashboard_screenshots/` PNG exports
- Cleaned CSV files in `data/processed/`

## Dependencies
Install dependencies before running ETL and EDA:
```bash
pip install -r requirements.txt
```

## Notes
- The ETL pipeline removes duplicates, standardizes dates, validates numeric values, and creates a production-ready SQLite data model.
- The notebook includes markdown explanations, observations, and business insights for every chart.

## Author
Capstone Project - Bluestock

## Date
June 4, 2026
