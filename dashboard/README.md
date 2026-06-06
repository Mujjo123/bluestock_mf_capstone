# Day 5 Dashboard Development

This folder contains the Day 5 dashboard deliverables for the Bluestock Mutual Fund Analytics Capstone Project.

## Purpose
Prepare dashboard-ready data and dashboard documentation for Power BI or Tableau.

## Files
- `dashboard_data_prep.py`: exports dashboard data CSVs and screenshot placeholders.
- `dashboard_summary.md`: describes dashboard pages, KPIs, filters, and data sources.

## How to use
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Generate dashboard data and screenshot placeholders:
   ```bash
   python dashboard/dashboard_data_prep.py
   ```
3. In Power BI or Tableau, connect to the CSV files in `dashboard/data/`.
4. Build dashboard pages for:
   - Executive summary KPIs
   - Performance comparisons
   - Risk / return analysis
   - Trend analysis
5. Export dashboard PNGs to `reports/dashboard_screenshots/`.

## Expected outputs
- `dashboard/data/*.csv`
- `reports/dashboard_screenshots/*.png`
- `dashboard/dashboard_summary.md`

## Notes
The dashboard is designed for a modern interactive build. If the raw or processed datasets are not available, the script will raise a missing file error and indicate which CSV is needed.
