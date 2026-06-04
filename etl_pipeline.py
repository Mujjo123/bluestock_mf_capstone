"""ETL pipeline for the Bluestock Mutual Fund Analytics Capstone Project."""

import sqlite3
from pathlib import Path
import pandas as pd
import numpy as np
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
DB_DIR = Path("data/db")
DB_PATH = DB_DIR / "bluestock_mf.db"
SCHEMA_PATH = Path("sql/schema.sql")

FILES = {
    "01_fund_master.csv": "fund_master",
    "02_nav_history.csv": "nav_history",
    "03_aum_by_fund_house.csv": "aum_by_fund_house",
    "04_monthly_sip_inflows.csv": "monthly_sip_inflows",
    "05_category_inflows.csv": "category_inflows",
    "06_industry_folio_count.csv": "industry_folio_count",
    "07_scheme_performance.csv": "scheme_performance",
    "08_investor_transactions.csv": "investor_transactions",
    "09_portfolio_holdings.csv": "portfolio_holdings",
    "10_benchmark_indices.csv": "benchmark_indices",
}

DATE_COLUMNS = {
    "fund_master": ["launch_date"],
    "nav_history": ["date"],
    "aum_by_fund_house": ["date"],
    "monthly_sip_inflows": ["month"],
    "category_inflows": ["month"],
    "industry_folio_count": ["month"],
    "investor_transactions": ["transaction_date"],
    "portfolio_holdings": ["portfolio_date"],
    "benchmark_indices": ["date"],
}

NUMERIC_COLUMNS = {
    "fund_master": [
        "expense_ratio_pct",
        "exit_load_pct",
        "min_sip_amount",
        "min_lumpsum_amount",
    ],
    "nav_history": ["nav"],
    "aum_by_fund_house": ["aum_lakh_crore", "aum_crore", "num_schemes"],
    "monthly_sip_inflows": [
        "sip_inflow_crore",
        "active_sip_accounts_crore",
        "new_sip_accounts_lakh",
        "sip_aum_lakh_crore",
        "yoy_growth_pct",
    ],
    "category_inflows": ["net_inflow_crore"],
    "industry_folio_count": [
        "total_folios_crore",
        "equity_folios_crore",
        "debt_folios_crore",
        "hybrid_folios_crore",
        "others_folios_crore",
    ],
    "scheme_performance": [
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "benchmark_3yr_pct",
        "alpha",
        "beta",
        "sharpe_ratio",
        "sortino_ratio",
        "std_dev_ann_pct",
        "max_drawdown_pct",
        "aum_crore",
        "expense_ratio_pct",
        "morningstar_rating",
    ],
    "investor_transactions": ["amount_inr", "annual_income_lakh"],
    "portfolio_holdings": ["weight_pct", "market_value_cr", "current_price_inr"],
    "benchmark_indices": ["close_value"],
}

CATEGORICAL_COLUMNS = {
    "fund_master": [
        "fund_house",
        "scheme_name",
        "category",
        "sub_category",
        "plan",
        "benchmark",
        "fund_manager",
        "risk_category",
    ],
    "category_inflows": ["category"],
    "scheme_performance": ["scheme_name", "fund_house", "category", "plan", "risk_grade"],
    "investor_transactions": [
        "transaction_type",
        "state",
        "city",
        "city_tier",
        "age_group",
        "gender",
        "payment_mode",
        "kyc_status",
    ],
    "portfolio_holdings": ["stock_symbol", "stock_name", "sector"],
    "benchmark_indices": ["index_name"],
}


def ensure_directories() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    DB_DIR.mkdir(parents=True, exist_ok=True)
    logging.info("Created necessary directories.")


def load_csv(filename: str) -> pd.DataFrame:
    file_path = RAW_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Missing raw file: {file_path}")

    df = pd.read_csv(file_path)
    logging.info("Loaded %s with shape %s", filename, df.shape)
    return df


def standardize_text_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        if column in df.columns:
            df[column] = (
                df[column]
                .astype(str)
                .str.strip()
                .replace({"nan": np.nan})
                .fillna("Unknown")
            )
    return df


def clean_dataframe(name: str, df: pd.DataFrame) -> pd.DataFrame:
    original_shape = df.shape
    df = df.drop_duplicates().reset_index(drop=True)
    logging.info("Removed duplicates for %s: %s -> %s", name, original_shape, df.shape)

    if name in DATE_COLUMNS:
        for date_col in DATE_COLUMNS[name]:
            if date_col in df.columns:
                df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
                logging.info("Converted %s.%s to datetime", name, date_col)

    if name in NUMERIC_COLUMNS:
        for numeric_col in NUMERIC_COLUMNS[name]:
            if numeric_col in df.columns:
                df[numeric_col] = pd.to_numeric(df[numeric_col], errors="coerce")
                if df[numeric_col].isna().any():
                    median_value = df[numeric_col].median(skipna=True)
                    fill_value = median_value if not np.isnan(median_value) else 0
                    df[numeric_col] = df[numeric_col].fillna(fill_value)
                    logging.info(
                        "Filled missing numeric values for %s.%s with %s",
                        name,
                        numeric_col,
                        fill_value,
                    )

    if name in CATEGORICAL_COLUMNS:
        df = standardize_text_columns(df, CATEGORICAL_COLUMNS[name])

    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    logging.info("Cleaned column names for %s", name)

    if df.isnull().sum().sum() > 0:
        null_summary = df.isnull().sum().sort_values(ascending=False)
        logging.info("Remaining missing values for %s:\n%s", name, null_summary[null_summary > 0].to_dict())

    return df


def save_cleaned_dataframe(name: str, df: pd.DataFrame) -> Path:
    output_path = PROCESSED_DIR / f"{name}.csv"
    df.to_csv(output_path, index=False)
    logging.info("Saved cleaned data to %s", output_path)
    return output_path


def build_and_save_cleaned_data() -> dict[str, Path]:
    ensure_directories()
    cleaned_files = {}
    for raw_name, clean_name in FILES.items():
        raw_df = load_csv(raw_name)
        cleaned_df = clean_dataframe(clean_name, raw_df)
        cleaned_path = save_cleaned_dataframe(clean_name, cleaned_df)
        cleaned_files[clean_name] = cleaned_path
    return cleaned_files


def create_sqlite_database() -> None:
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Schema file does not exist: {SCHEMA_PATH}")

    with sqlite3.connect(DB_PATH) as conn:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
            schema_sql = schema_file.read()
        conn.executescript(schema_sql)
        logging.info("Initialized SQLite database at %s", DB_PATH)


def load_cleaned_data_to_sqlite(cleaned_files: dict[str, Path]) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        for table_name, file_path in cleaned_files.items():
            df = pd.read_csv(file_path)
            df_columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
            df.columns = df_columns
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            logging.info("Loaded table %s with %s rows", table_name, len(df))


def run_etl() -> None:
    logging.info("Starting ETL pipeline")
    cleaned_files = build_and_save_cleaned_data()
    create_sqlite_database()
    load_cleaned_data_to_sqlite(cleaned_files)
    logging.info("ETL pipeline completed successfully")


if __name__ == "__main__":
    run_etl()
