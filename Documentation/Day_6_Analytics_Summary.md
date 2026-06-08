# Day 6: Advanced Analytics & Risk Metrics
## Bluestock Mutual Fund Analytics Capstone

**Date**: June 8, 2026  
**Notebook**: `notebooks/Day_6_Advanced_Analytics.ipynb`

---

## Overview

Day 6 delivers a comprehensive advanced analytics pipeline that performs sophisticated risk measurement, benchmark analysis, and investor demographic profiling. The notebook ingests cleaned datasets and produces professional-grade analytical reports.

---

## Key Analytics Performed

### 1. Risk & Performance Metrics

#### Sharpe Ratio
- **Definition**: Excess return per unit of risk (volatility)
- **Formula**: (Annual Return - Risk-Free Rate) / Annual Volatility
- **Interpretation**: Higher Sharpe ratio indicates better risk-adjusted returns
- **Use Case**: Portfolio construction, fund selection, performance ranking

#### Sortino Ratio
- **Definition**: Excess return per unit of downside risk only
- **Formula**: (Annual Return - Risk-Free Rate) / Downside Deviation
- **Interpretation**: More penalizes downside losses than total volatility
- **Use Case**: Risk-averse investor profiles, downside protection analysis

#### Value at Risk (VaR 95%)
- **Definition**: Daily loss threshold at 95% confidence level
- **Formula**: 5th percentile of daily returns distribution
- **Interpretation**: "95% of the time, daily losses are less than X%"
- **Use Case**: Risk limit setting, stress testing, capital allocation

#### Maximum Drawdown
- **Definition**: Peak-to-trough decline from historical high to low
- **Detection**: Identifies the date range and magnitude of largest decline
- **Interpretation**: Worst-case scenario for buy-and-hold investor
- **Use Case**: Psychological impact assessment, worst-case planning

#### Annualized Return & Volatility
- **Return**: Annualized average daily percentage change
- **Volatility**: Annualized standard deviation of returns
- **Combined**: Basis for risk-return analysis

### 2. Benchmark Analysis

#### Alpha Calculation
- **Definition**: Excess return not explained by market movement
- **Formula**: Intercept from fund return vs benchmark return regression
- **Annualization**: Multiplied by 252 trading days
- **Interpretation**: Positive alpha = fund manager skill, Negative alpha = underperformance
- **Note**: Should exceed management fees and transaction costs

#### Beta Calculation
- **Definition**: Sensitivity to benchmark movement
- **Formula**: Slope from fund return vs benchmark return regression
- **Interpretation**: 
  - Beta = 1.0: Moves in line with benchmark
  - Beta < 1.0: Less volatile than benchmark (defensive)
  - Beta > 1.0: More volatile than benchmark (aggressive)

#### Tracking Error
- **Definition**: Standard deviation of fund return minus benchmark return
- **Formula**: Annualized std of active return (fund - benchmark)
- **Interpretation**: Precision of fund manager strategy implementation
- **Use Case**: Active vs passive strategy assessment

#### Rolling Correlation
- **Definition**: 60-day rolling correlation between fund and benchmark
- **Interpretation**: Varies over time; helps identify regime changes
- **Use Case**: Portfolio diversification assessment

### 3. Investor Demographics

#### Age Distribution
- Segments investors into age brackets: <25, 25-35, 35-45, 45-55, 55+
- Reveals target demographic and investment maturity profile

#### Income Bucket Analysis
- Categorizes investors by income levels
- Identifies primary market segment (mass, middle, affluent, HNI)

#### State-wise Distribution
- Top 15 states showing geographic market penetration
- Identifies concentration and expansion opportunities

#### SIP vs Lumpsum
- Regular investment (SIP) vs one-time investment (Lumpsum)
- SIP-heavy indicates long-term wealth building; Lumpsum indicates event-driven investing

#### City Tier Classification
- Tier 1: Major metros (Delhi, Mumbai, Bangalore, etc.)
- Tier 2: Secondary cities
- Tier 3: Smaller cities
- Shows market expansion opportunities

#### Gender Distribution
- Female vs male investors (if available)
- Diversity and inclusion metrics

---

## Output Files Generated

### CSV Reports

| File | Purpose | Key Columns |
|------|---------|-------------|
| `fund_sharpe_ranks.csv` | Comprehensive fund rankings | AMFI Code, Scheme Name, Return, Volatility, Sharpe, Sortino, VaR 95%, Ranks |
| `var_drawdown_summary.csv` | Risk metrics summary | AMFI Code, VaR 95%, Max Drawdown, Drawdown Dates |
| `alpha_beta_table.csv` | Benchmark regression results | AMFI Code, Benchmark, Alpha, Beta, Tracking Error, R² |
| `rolling_correlations.csv` | Fund-to-benchmark correlations | AMFI Code, Benchmark, Avg Correlation, Correlation Std Dev |

### Interactive Charts (HTML)

| Chart | Purpose | Insights |
|-------|---------|----------|
| `risk_return_scatter.html` | Visual fund positioning | Portfolio construction, efficient frontier |
| `sharpe_ratio_ranking.html` | Top performers | Best risk-adjusted returns (top 20) |
| `alpha_beta_comparison.html` | Manager skill assessment | Alpha generation vs market sensitivity |
| `state_distribution.html` | Geographic reach | Market penetration by state |
| `sip_lumpsum_distribution.html` | Investment behavior | Regular vs event-driven investing |
| `income_distribution.html` | Investor profile | Target market segment |
| `benchmark_comparison.html` | Index performance | Benchmark selection rationale |

### Markdown Reports

| File | Content |
|------|---------|
| `Day_6_Insights.md` | Business insights, key findings, recommendations |

---

## How to Run

### Option 1: Comprehensive Jupyter Notebook (Recommended)
```bash
cd notebooks
jupyter notebook Day_6_Advanced_Analytics.ipynb
```
- Provides interactive exploration
- Allows parameter tweaking
- Shows all intermediate calculations
- Generates all charts and reports

### Option 2: Command-line Script
```bash
python scripts/advanced_analytics.py
```
- Faster execution
- Batch processing
- Scheduled analysis
- Production deployment

---

## Constants & Assumptions

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Risk-Free Rate | 6.5% | Current RBI repo rate |
| Trading Days | 252 | Annual trading days in India |
| VaR Confidence Level | 95% | Standard in risk management |
| Correlation Window | 60 days | Balance between responsiveness and stability |
| Minimum Observations | 20 | Sufficient data for regression |

---

## Data Requirements

The notebook expects cleaned CSV files in either `data/processed/` or `data/raw/`:

1. **01_fund_master.csv**: Fund metadata (AMFI code, scheme name, fund house)
2. **02_nav_history.csv**: Daily NAV with date and value
3. **07_scheme_performance.csv**: Scheme performance data
4. **08_investor_transactions.csv**: Investor demographics and transactions
5. **10_benchmark_indices.csv**: Daily benchmark closing values (Nifty 50, 100, Midcap 150, SmallCap)

---

## Interpretation Guide

### Risk-Return Scatter Plot
- **Upper Right Quadrant**: High return, high risk (aggressive growth funds)
- **Upper Left Quadrant**: High return, low risk (efficient funds)
- **Lower Left Quadrant**: Low return, low risk (conservative funds)
- **Lower Right Quadrant**: Low return, high risk (avoid)

### Sharpe Ratio Rankings
- **>2.0**: Excellent risk-adjusted returns
- **1.0-2.0**: Good risk-adjusted returns
- **0-1.0**: Acceptable risk-adjusted returns
- **<0**: Underperforming risk-free rate

### Alpha Interpretation
- **Positive & Large**: Fund manager generates value
- **Positive & Small**: Barely beats after fees
- **Negative**: Underperformance after fees
- **High R²**: Explains beta; low R² = unique skill

### Beta Interpretation
- **0.7-0.9**: Defensive equity
- **1.0-1.2**: Index-like behavior
- **1.2+**: Aggressive/growth-oriented
- **<1.0**: Lower market sensitivity

---

## Business Recommendations

1. **For Portfolio Managers**:
   - Use top Sharpe/Sortino funds as core holdings
   - Monitor alpha generation for fund selection
   - Track maximum drawdown for stress scenarios

2. **For Investors**:
   - Compare funds on risk-adjusted basis (Sharpe), not just returns
   - Consider Sortino for downside protection preference
   - Use VaR for portfolio stress testing

3. **For Marketing**:
   - Highlight top performers in Sharpe/Sortino rankings
   - Emphasize state-wise growth opportunities
   - Target income segments based on fund categories

4. **For Risk Management**:
   - Monitor VaR limits against portfolio allocation
   - Track rolling correlations for diversification effectiveness
   - Set drawdown triggers for rebalancing

---

## Limitations & Caveats

1. **Historical Data**: Past performance doesn't guarantee future results
2. **Normality Assumption**: VaR assumes normal distribution (extreme events may exceed VaR)
3. **Correlation Stationarity**: Rolling correlation may change in crisis periods
4. **Benchmark Selection**: Alpha/Beta valid only for appropriate benchmark choice
5. **Data Quality**: Results depend on clean, accurate input data

---

## Files Modified/Created

- ✅ `notebooks/Day_6_Advanced_Analytics.ipynb` - Main comprehensive notebook
- ✅ `scripts/advanced_analytics.py` - Lightweight pipeline script
- ✅ `Documentation/Day_6_Analytics_Summary.md` - This file
- ✅ `README.md` - Updated with Day 6 instructions
- ✅ Output reports in `reports/` directory

---

## Next Steps (Day 7)

- Integration with Power BI dashboard
- Automated report scheduling
- Real-time monitoring dashboard
- Alert system for threshold breaches
- Mobile app for investor access

---

**Status**: ✅ Complete  
**Execution Time**: Depends on data volume (typically 5-10 minutes for full analysis)  
**Dependencies**: pandas, numpy, scipy, plotly, seaborn, matplotlib
