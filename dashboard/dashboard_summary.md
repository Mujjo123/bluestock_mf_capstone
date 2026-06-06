# Day 5 Dashboard Development Summary

This dashboard is designed for the Bluestock Mutual Fund Analytics Capstone Project using Day 2, Day 3, and Day 4 outputs.

## Dashboard Overview
The dashboard is built to highlight fund performance, risk metrics, investment trends, and portfolio distribution. It is intended to be deployed in Power BI or Tableau with the exported dataset files in `dashboard/data/`.

## Pages and KPIs

### 1. Executive Summary Page
- **Total AUM**: aggregate AUM across all funds, derived from scheme performance or AUM-by-fund-house data.
- **Average NAV**: average NAV across all schemes in the NAV history.
- **Top 10 Funds by AUM**: largest schemes by AUM, shown with fund house and category.
- **Fund Performance Scorecard**: rank-based scorecard combining CAGR, Sharpe, alpha, expense ratio, and drawdown.

### 2. Fund Performance Comparison
- **CAGR Comparison**: compare 1-year, 3-year, and 5-year CAGR for funds.
- **Sharpe Ratio Comparison**: relative risk-adjusted returns across active schemes.
- **Alpha and Beta Analysis**: benchmark-adjusted performance for funds relative to Nifty indices.

### 3. Risk & Return Analytics
- **Risk vs Return Scatter Plot**: Sharpe ratio versus downside or volatility measures from scheme performance.
- **Fund House Distribution**: AUM and scheme counts by fund house, showing concentration and balance.

### 4. Trend Analysis
- **Monthly SIP Trend**: trend line for SIP inflows and SIP AUM over time.
- **NAV Trend Analysis**: NAV history for top funds, showing fund trajectory and cycle behavior.

## Filters
The dashboard includes the following filters to support interactive analysis:
- **Fund House**: filter all visuals by the asset manager / fund house.
- **Scheme Category**: filter by scheme category to compare equity, debt, hybrid, and specialty strategies.
- **Date Range**: filter time-series charts, benchmark analysis, and NAV trends by date.

## Data Sources
The following data sources are prepared for dashboard consumption:
- `dashboard/data/total_aum.csv`
- `dashboard/data/average_nav.csv`
- `dashboard/data/top_10_funds_by_aum.csv`
- `dashboard/data/cagr_comparison.csv`
- `dashboard/data/sharpe_comparison.csv`
- `dashboard/data/fund_house_distribution.csv`
- `dashboard/data/monthly_sip_trend.csv`
- `dashboard/data/nav_trend.csv`
- `dashboard/data/risk_return_scatter.csv`
- `dashboard/data/alpha_beta.csv`
- `dashboard/data/fund_scorecard.csv`

## Dashboard Screenshots
Placeholder dashboard screenshot files are exported to `reports/dashboard_screenshots/`.

## How to Use
1. Run `python dashboard/dashboard_data_prep.py` to generate dashboard-ready CSV files and screenshot placeholders.
2. Open Power BI Desktop or Tableau.
3. Connect to the CSV files in `dashboard/data/`.
4. Build pages using the KPI and chart definitions above.
5. Apply filters for Fund House, Scheme Category, and Date Range.
6. Export dashboard images to `reports/dashboard_screenshots/`.

## Notes
- The data prep script is robust to either `data/processed/` or `data/raw/` datasets.
- If `reports/alpha_beta.csv` or `reports/fund_scorecard.csv` already exists, they are used directly.
- The script also generates placeholder PNGs so the dashboard deliverable directory is populated with sample exports.
