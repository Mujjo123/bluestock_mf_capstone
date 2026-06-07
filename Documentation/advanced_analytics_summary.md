# Day 6 — Advanced Analytics and Risk Metrics

This document summarizes the Day 6 advanced analytics deliverables for the Bluestock Mutual Fund Analytics Capstone.

## Objective
Compute advanced benchmark and risk metrics across all mutual fund schemes and support visualization for performance benchmarking.

## Key Deliverables
- `reports/alpha_beta_table.csv`
- `reports/fund_sharpe_ranks.csv`
- `reports/var_drawdown_summary.csv`
- Chart exports in `reports/advanced_charts/`
  - `benchmark_comparison.png`
  - `risk_return_scatter.png`
  - `alpha_beta_comparison.png`
- Notebook: `notebooks/advanced_analytics.ipynb`
- Script: `scripts/advanced_analytics.py`

## Analytics Covered
- Daily returns per scheme using historical NAV data
- Sharpe ratio and Sortino ratio for all funds
- 95% Value at Risk (VaR) based on daily returns
- Maximum drawdown and drawdown period detection
- Alpha/Beta regression versus benchmark indices
- Risk-return scatter analysis for fund comparison

## Usage
1. Populate `data/raw/` or `data/processed/` with cleaned datasets.
2. Run the advanced analytics pipeline:
   ```bash
   python scripts/advanced_analytics.py
   ```
3. Review generated CSV outputs in `reports/`.
4. Open the notebook for interactive analysis and result review:
   ```bash
   jupyter notebook notebooks/advanced_analytics.ipynb
   ```

## Notes
- The script uses benchmark indices: `Nifty 50`, `Nifty 100`, `Nifty Midcap 150`, and `BSE SmallCap`.
- When plotting dependencies are missing, the script writes chart placeholders instead of live visualizations.
- Output files are saved to `reports/` and chart placeholders save to `reports/advanced_charts/`.
