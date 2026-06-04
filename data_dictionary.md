# Bluestock Mutual Fund Analytics Data Dictionary

## 01_fund_master.csv
- amfi_code: Unique identifier assigned by AMFI
- fund_house: Asset management company name
- scheme_name: Mutual fund scheme name
- category: Fund category (e.g. Large Cap, Hybrid, Debt)
- sub_category: More granular scheme classification
- plan: Direct or regular plan type
- launch_date: Fund launch date
- benchmark: Benchmark index for the scheme
- expense_ratio_pct: Expense ratio percentage
- exit_load_pct: Exit load percentage
- min_sip_amount: Minimum SIP amount required
- min_lumpsum_amount: Minimum lumpsum investment amount
- fund_manager: Fund manager name
- risk_category: Risk profile label
- sebi_category_code: SEBI category code

## 02_nav_history.csv
- amfi_code: Scheme identifier for NAV record
- date: NAV observation date
- nav: Net asset value for the scheme on the date

## 03_aum_by_fund_house.csv
- date: Reporting date
- fund_house: Asset management company name
- aum_lakh_crore: AUM in lakh crore
- aum_crore: AUM in crore
- num_schemes: Number of schemes reported for the fund house

## 04_monthly_sip_inflows.csv
- month: Calendar month of SIP inflows
- sip_inflow_crore: Monthly SIP inflow value in crores
- active_sip_accounts_crore: Active SIP accounts in crores
- new_sip_accounts_lakh: New SIP accounts added in lakhs
- sip_aum_lakh_crore: AUM from SIP investments in lakh crore
- yoy_growth_pct: Year-over-year growth percentage

## 05_category_inflows.csv
- month: Reporting month
- category: Fund category name
- net_inflow_crore: Net inflow value in crores for the category

## 06_industry_folio_count.csv
- month: Reporting month
- total_folios_crore: Total folio count in crores
- equity_folios_crore: Equity folios in crores
- debt_folios_crore: Debt folios in crores
- hybrid_folios_crore: Hybrid folios in crores
- others_folios_crore: Other folios in crores

## 07_scheme_performance.csv
- amfi_code: Scheme identifier
- scheme_name: Mutual fund scheme name
- fund_house: Asset management company name
- category: Fund category
- plan: Direct or regular plan type
- return_1yr_pct: One-year return percentage
- return_3yr_pct: Three-year return percentage
- return_5yr_pct: Five-year return percentage
- benchmark_3yr_pct: Benchmark return over three years
- alpha: Alpha value relative to benchmark
- beta: Beta value relative to benchmark
- sharpe_ratio: Sharpe ratio for the scheme
- sortino_ratio: Sortino ratio for the scheme
- std_dev_ann_pct: Annualized standard deviation percentage
- max_drawdown_pct: Maximum drawdown percentage
- aum_crore: Total AUM in crores for the scheme
- expense_ratio_pct: Expense ratio percentage
- morningstar_rating: Morningstar rating
- risk_grade: Risk grade label

## 08_investor_transactions.csv
- investor_id: Unique transaction investor identifier
- transaction_date: Transaction date
- amfi_code: Scheme identifier for the transaction
- transaction_type: Transaction category (e.g. purchase, redemption)
- amount_inr: Transaction amount in rupees
- state: Investor state
- city: Investor city
- city_tier: City tier classification
- age_group: Age bracket of investor
- gender: Investor gender
- annual_income_lakh: Annual income in lakhs
- payment_mode: Transaction payment type
- kyc_status: KYC completion status

## 09_portfolio_holdings.csv
- amfi_code: Scheme identifier for portfolio holdings
- stock_symbol: Stock ticker symbol
- stock_name: Company name
- sector: Industry sector classification
- weight_pct: Scheme allocation percentage
- market_value_cr: Market value in crores
- current_price_inr: Stock price in rupees
- portfolio_date: Portfolio as-of date

## 10_benchmark_indices.csv
- date: Index observation date
- index_name: Benchmark index name (NIFTY50, NIFTY100, etc.)
- close_value: Closing index value

## Notes
- Cleaned datasets are saved to `data/processed/`.
- The SQLite database file is created at `data/db/bluestock_mf.db`.
- SQL schema and analytical queries are stored in `sql/schema.sql` and `sql/queries.sql`.
