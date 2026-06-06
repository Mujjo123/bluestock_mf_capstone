# Day 5 Dashboard Development Summary

This dashboard is designed for the Bluestock Mutual Fund Analytics Capstone Project using Day 1–Day 4 outputs.

## Dashboard Purpose
Create a Power BI dashboard with four pages that summarize market conditions, fund performance, investor demographics, and portfolio holdings.

## Dashboard Pages

### Page 1 — Market Overview
- **Industry AUM**: total AUM across funds and asset managers.
- **SIP Inflows**: monthly SIP flows over time.
- **Folio Growth**: folio count growth trends, drawing from industry and investor data.
- **Category-wise Inflows**: category-level net flows and trend comparisons.

### Page 2 — Fund Performance & Risk
- **Sharpe Ratio**: risk-adjusted return across active schemes.
- **Sortino Ratio**: downside-risk adjusted performance.
- **Alpha**: excess return relative to benchmark indices.
- **Beta**: sensitivity to benchmark movements.
- **Max Drawdown**: worst peak-to-trough decline by scheme.

### Page 3 — Investor Demographics
- **Age Distribution**: investor age group composition.
- **Income Distribution**: investor income segment mix.
- **State-wise Investors**: geographic investor concentration.
- **SIP vs Lumpsum**: comparative volume of systematic investment plans versus lumpsum transactions.

### Page 4 — Portfolio Holdings
- **Sector Exposure**: holdings weighted by sector.
- **Top Holdings**: largest stock or asset holdings by scheme.
- **Fund-wise Allocation**: allocation breakdown across schemes and categories.

## Filters
- **Fund House**
- **Scheme Category**
- **Date Range**

## Data Sources
The dashboard uses prepared CSV exports from the project:
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

## Screenshots
The four dashboard page screenshot placeholders are available in `reports/dashboard_screenshots/`.

## How to Use
1. Run `python dashboard/dashboard_data_prep.py` to refresh exports and screenshots.
2. Open Power BI Desktop.
3. Connect to the CSV files in `dashboard/data/`.
4. Build the four pages described above.
5. Export dashboard screenshots to `reports/dashboard_screenshots/`.

## Deliverables
- `dashboard/dashboard.pbix` (Power BI dashboard placeholder)
- `dashboard/dashboard_summary.md`
- `dashboard/data/*.csv`
- `reports/dashboard_screenshots/*.png`
- `Documentation/dashboard_summary.md`

## Notes
- The placeholder Power BI file is included for deliverable structure. Replace it with the actual `.pbix` file when the dashboard is built in Power BI Desktop.
