"""
Live NAV Fetch Script for Bluestock MF Capstone Project
Fetches latest NAV data from mfapi.in
"""

import requests
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import time

# Define data directory
DATA_RAW = Path(__file__).parent.parent / "data" / "raw"
DATA_PROCESSED = Path(__file__).parent.parent / "data" / "processed"

# MFAPI endpoints
MFAPI_BASE_URL = "https://api.mfapi.in"

def fetch_mf_list():
    """Fetch list of all mutual funds from MFAPI"""
    
    print("=" * 80)
    print("LIVE NAV FETCHING FROM MFAPI.IN")
    print("=" * 80)
    print()
    
    try:
        print("📥 Fetching mutual fund list from mfapi.in...")
        response = requests.get(f"{MFAPI_BASE_URL}/mf", timeout=10)
        response.raise_for_status()
        
        mf_data = response.json()
        print(f"✅ Successfully fetched {len(mf_data)} mutual funds")
        
        return mf_data
    
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Failed to fetch MF list")
        print(f"   Error: {str(e)}")
        return None

def fetch_nav_for_scheme(scheme_code):
    """Fetch NAV history for a specific scheme"""
    
    try:
        response = requests.get(
            f"{MFAPI_BASE_URL}/mf/{scheme_code}",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        return None

def process_live_nav_data(mf_list):
    """Process and save live NAV data"""
    
    if not mf_list:
        print("❌ No data to process")
        return
    
    print("\n" + "="*80)
    print("PROCESSING LIVE NAV DATA")
    print("="*80)
    
    nav_data_list = []
    processed_count = 0
    error_count = 0
    
    # Sample first 10 funds (to avoid rate limiting)
    sample_funds = mf_list[:10] if len(mf_list) > 10 else mf_list
    
    print(f"\n📊 Processing {len(sample_funds)} mutual funds...")
    
    for idx, fund in enumerate(sample_funds, 1):
        scheme_code = fund.get('schemeCode')
        scheme_name = fund.get('schemeName')
        
        print(f"\n   [{idx}/{len(sample_funds)}] Processing: {scheme_name}")
        
        nav_details = fetch_nav_for_scheme(scheme_code)
        
        if nav_details and 'nav' in nav_details:
            nav_list = nav_details['nav']
            
            if nav_list:
                # Get latest NAV
                latest_nav = nav_list[0] if nav_list else {}
                
                nav_data_list.append({
                    'Scheme_Code': scheme_code,
                    'Scheme_Name': scheme_name,
                    'Latest_NAV': latest_nav.get('nav', 'N/A'),
                    'Date': latest_nav.get('date', 'N/A'),
                    'Total_NAV_Records': len(nav_list),
                    'Status': 'Success'
                })
                
                print(f"      ✅ Latest NAV: {latest_nav.get('nav', 'N/A')} | Date: {latest_nav.get('date', 'N/A')}")
                processed_count += 1
        else:
            nav_data_list.append({
                'Scheme_Code': scheme_code,
                'Scheme_Name': scheme_name,
                'Latest_NAV': 'N/A',
                'Date': 'N/A',
                'Total_NAV_Records': 0,
                'Status': 'Failed'
            })
            error_count += 1
            print(f"      ❌ Failed to fetch NAV")
        
        # Add small delay to avoid rate limiting
        time.sleep(0.5)
    
    # Create DataFrame and save
    if nav_data_list:
        nav_df = pd.DataFrame(nav_data_list)
        
        # Save to CSV
        output_file = DATA_PROCESSED / "live_nav_data.csv"
        nav_df.to_csv(output_file, index=False)
        
        print("\n" + "="*80)
        print("LIVE NAV SUMMARY")
        print("="*80)
        print(f"\n✅ Successfully processed: {processed_count}")
        print(f"❌ Failed to process: {error_count}")
        print(f"📁 File saved to: {output_file}")
        print("\nFirst 5 Records:")
        print(nav_df.head().to_string(index=False))
    
    print("\n" + "="*80)
    print("✅ LIVE NAV FETCH COMPLETE")
    print("="*80)

def main():
    """Main execution function"""
    
    print("\n🚀 Starting Live NAV Fetch Process...")
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Fetch MF list
    mf_list = fetch_mf_list()
    
    if mf_list:
        # Process NAV data
        process_live_nav_data(mf_list)
    else:
        print("\n⚠️  WARNING: Could not fetch MF list. Please check your internet connection.")
        print("   MFAPI might be rate limiting or temporarily unavailable.")
        print("\n💡 TIP: You can manually place NAV data in data/raw/ folder or update the script later.")

if __name__ == "__main__":
    main()
