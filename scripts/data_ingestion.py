"""
Data Ingestion Script for Bluestock MF Capstone Project
Loads and validates all 10 CSV datasets
"""

import pandas as pd
import os
from pathlib import Path

# Define data directory
DATA_RAW = Path(__file__).parent.parent / "data" / "raw"
DATA_PROCESSED = Path(__file__).parent.parent / "data" / "processed"

# List of CSV files to load
CSV_FILES = [
    "01_fund_master.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv"
]

def load_and_validate_data():
    """Load all CSV files and perform validation"""
    
    print("=" * 80)
    print("BLUESTOCK MF CAPSTONE - DATA INGESTION")
    print("=" * 80)
    print()
    
    loaded_datasets = {}
    data_quality_report = []
    
    for csv_file in CSV_FILES:
        file_path = DATA_RAW / csv_file
        
        print(f"\n{'='*80}")
        print(f"Loading: {csv_file}")
        print(f"{'='*80}")
        
        try:
            # Load CSV
            if not file_path.exists():
                print(f"⚠️  WARNING: File not found at {file_path}")
                print(f"   Please ensure CSV file is placed in: {DATA_RAW}/")
                continue
            
            df = pd.read_csv(file_path)
            loaded_datasets[csv_file] = df
            
            # Print Dataset Info
            print(f"✅ Status: Successfully Loaded")
            print(f"\n📊 Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")
            
            # Print Data Types
            print(f"\n📋 Column Data Types:")
            print(df.dtypes)
            
            # Print First Few Rows
            print(f"\n📈 First 5 Rows:")
            print(df.head())
            
            # Data Quality Checks
            print(f"\n🔍 Data Quality Metrics:")
            print(f"   - Missing Values: {df.isnull().sum().sum()}")
            print(f"   - Duplicate Rows: {df.duplicated().sum()}")
            print(f"   - Memory Usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
            
            # Store quality metrics
            data_quality_report.append({
                'File': csv_file,
                'Rows': df.shape[0],
                'Columns': df.shape[1],
                'Missing_Values': df.isnull().sum().sum(),
                'Duplicates': df.duplicated().sum(),
                'Status': 'Loaded'
            })
            
        except Exception as e:
            print(f"❌ ERROR: Failed to load {csv_file}")
            print(f"   Error: {str(e)}")
            data_quality_report.append({
                'File': csv_file,
                'Rows': 0,
                'Columns': 0,
                'Missing_Values': 0,
                'Duplicates': 0,
                'Status': f'Error: {str(e)[:50]}'
            })
    
    # Summary Report
    print(f"\n\n{'='*80}")
    print("DATA INGESTION SUMMARY REPORT")
    print(f"{'='*80}")
    
    summary_df = pd.DataFrame(data_quality_report)
    print(summary_df.to_string(index=False))
    
    # Overall Statistics
    print(f"\n\n📌 OVERALL STATISTICS:")
    print(f"   - Total Files Loaded: {len(loaded_datasets)}/{len(CSV_FILES)}")
    print(f"   - Total Rows Loaded: {sum([df.shape[0] for df in loaded_datasets.values()])}")
    print(f"   - Total Columns: {sum([df.shape[1] for df in loaded_datasets.values()])}")
    
    # Save summary report
    summary_df.to_csv(DATA_PROCESSED / "data_ingestion_report.csv", index=False)
    print(f"\n✅ Report saved to: {DATA_PROCESSED}/data_ingestion_report.csv")
    
    print("\n" + "="*80)
    print("✅ DATA INGESTION COMPLETE")
    print("="*80)
    
    return loaded_datasets

if __name__ == "__main__":
    datasets = load_and_validate_data()
