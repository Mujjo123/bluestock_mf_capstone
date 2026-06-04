-- Top 5 funds by AUM
SELECT f.fund_house,
       f.scheme_name,
       a.aum_crore
FROM dim_fund f
JOIN fact_aum a ON f.fund_house = a.fund_house
ORDER BY a.aum_crore DESC
LIMIT 5;

-- Average NAV by month
SELECT strftime('%Y-%m', nav_date) AS month,
       AVG(nav) AS avg_nav
FROM fact_nav
GROUP BY month
ORDER BY month;

-- SIP growth trend
SELECT month,
       sip_inflow_crore,
       active_sip_accounts_crore,
       new_sip_accounts_lakh,
       sip_aum_lakh_crore,
       yoy_growth_pct
FROM fact_sip_industry
ORDER BY month;

-- State-wise transactions
SELECT state,
       COUNT(*) AS transaction_count,
       SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;

-- Expense ratio analysis by fund house
SELECT fund_house,
       AVG(expense_ratio_pct) AS avg_expense_ratio
FROM dim_fund
GROUP BY fund_house
ORDER BY avg_expense_ratio DESC;

-- Fund performance comparison
SELECT scheme_name,
       return_1yr_pct,
       return_3yr_pct,
       return_5yr_pct
FROM fact_performance
ORDER BY return_3yr_pct DESC
LIMIT 15;

-- Alpha / Beta comparison
SELECT scheme_name,
       alpha,
       beta
FROM fact_performance
WHERE alpha IS NOT NULL
ORDER BY alpha DESC
LIMIT 15;

-- Sharpe ratio ranking
SELECT scheme_name,
       sharpe_ratio
FROM fact_performance
WHERE sharpe_ratio IS NOT NULL
ORDER BY sharpe_ratio DESC
LIMIT 15;

-- Investor demographic analysis
SELECT age_group,
       gender,
       COUNT(*) AS transactions,
       SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY age_group,
         gender
ORDER BY total_amount DESC
LIMIT 20;

-- Category inflow analysis
SELECT category,
       SUM(net_inflow_crore) AS total_inflow
FROM category_inflows
GROUP BY category
ORDER BY total_inflow DESC;

-- Benchmark index comparison for top indices
SELECT index_name,
       AVG(close_value) AS avg_close_value
FROM benchmark_indices
GROUP BY index_name
ORDER BY avg_close_value DESC
LIMIT 10;

-- Top portfolio sectors by holding value
SELECT sector,
       SUM(market_value_cr) AS total_market_value_cr
FROM portfolio_holdings
GROUP BY sector
ORDER BY total_market_value_cr DESC
LIMIT 10;
