# Day 5 Dashboard Development

This folder contains the Day 5 dashboard deliverables for the Bluestock Mutual Fund Analytics Capstone Project.

## Purpose
Prepare Power BI dashboard data, documentation, and placeholder deliverables for the four requested pages.

## Files
- `dashboard_data_prep.py`: exports dashboard data CSVs and screenshot placeholders.
- `dashboard_summary.md`: describes dashboard page definitions, KPIs, filters, and data sources.
- `dashboard.pbix`: placeholder Power BI dashboard file for repository deliverable structure.

## Dashboard pages
1. Market Overview
2. Fund Performance & Risk
3. Investor Demographics
4. Portfolio Holdings

## How to use
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Generate dashboard data and screenshot placeholders:
   ```bash
   python dashboard/dashboard_data_prep.py
   ```
3. Open Power BI Desktop.
4. Connect to the CSV files in `dashboard/data/`.
5. Build the dashboard pages using the definitions in `dashboard/dashboard_summary.md`.
6. Export dashboard PNGs to `reports/dashboard_screenshots/`.

## Expected outputs
- `dashboard/data/*.csv`
- `reports/dashboard_screenshots/*.png`
- `dashboard/dashboard.pbix`
- `dashboard/dashboard_summary.md`

## Notes
The placeholder `.pbix` file is included for deliverable completeness. Replace it with an actual Power BI file after building the dashboard in Power BI Desktop.
