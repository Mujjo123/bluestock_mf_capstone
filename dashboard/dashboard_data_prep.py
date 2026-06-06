"""Dashboard data preparation for Day 5 of the Bluestock Mutual Fund Analytics Capstone."""

from pathlib import Path
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / 'data' / 'raw'
PROCESSED_DIR = ROOT / 'data' / 'processed'
REPORTS_DIR = ROOT / 'reports'
DASHBOARD_DATA_DIR = Path(__file__).resolve().parent / 'data'
SCREENSHOT_DIR = REPORTS_DIR / 'dashboard_screenshots'

DASHBOARD_DATA_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

DATA_FILES = {
    'fund_master': '01_fund_master.csv',
    'nav_history': '02_nav_history.csv',
    'aum_by_fund_house': '03_aum_by_fund_house.csv',
    'monthly_sip_inflows': '04_monthly_sip_inflows.csv',
    'category_inflows': '05_category_inflows.csv',
    'scheme_performance': '07_scheme_performance.csv',
    'alpha_beta': 'alpha_beta.csv',
    'fund_scorecard': 'fund_scorecard.csv',
}


def load_dataframe(filename: str) -> pd.DataFrame:
    processed_path = PROCESSED_DIR / filename
    raw_path = RAW_DIR / filename
    report_path = REPORTS_DIR / filename
    load_order = [processed_path, raw_path, report_path]
    for path in load_order:
        if path.exists():
            df = pd.read_csv(path, parse_dates=True)
            df.columns = [str(col).strip().lower().replace(' ', '_') for col in df.columns]
            return df
    print(f'Warning: missing dataset {filename}; using empty dataframe placeholder.')
    return pd.DataFrame()


def compute_total_aum(scheme_perf: pd.DataFrame, aum_by_fund_house: pd.DataFrame) -> pd.DataFrame:
    if 'aum_crore' in scheme_perf.columns:
        total_aum = scheme_perf['aum_crore'].sum()
    elif 'aum_crore' in aum_by_fund_house.columns:
        total_aum = aum_by_fund_house['aum_crore'].sum()
    else:
        total_aum = None
    return pd.DataFrame([{'total_aum_crore': total_aum}])


def compute_average_nav(nav: pd.DataFrame) -> pd.DataFrame:
    if 'nav' in nav.columns:
        avg_nav = nav['nav'].mean()
    else:
        avg_nav = None
    return pd.DataFrame([{'average_nav': avg_nav}])


def export_top_10_aum(scheme_perf: pd.DataFrame) -> pd.DataFrame:
    if 'aum_crore' not in scheme_perf.columns:
        return pd.DataFrame()
    top10 = scheme_perf.sort_values('aum_crore', ascending=False).head(10)
    return top10[['scheme_name', 'fund_house', 'category', 'aum_crore', 'sharpe_ratio']].copy()


def export_cagr_comparison(scheme_perf: pd.DataFrame) -> pd.DataFrame:
    columns = [col for col in ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct'] if col in scheme_perf.columns]
    if not columns:
        return pd.DataFrame()
    return scheme_perf[['amfi_code', 'scheme_name', 'fund_house', 'category'] + columns].copy()


def export_sharpe_comparison(scheme_perf: pd.DataFrame) -> pd.DataFrame:
    if 'sharpe_ratio' not in scheme_perf.columns:
        return pd.DataFrame()
    return scheme_perf[['amfi_code', 'scheme_name', 'fund_house', 'category', 'sharpe_ratio']].copy()


def export_fund_house_distribution(scheme_perf: pd.DataFrame) -> pd.DataFrame:
    if 'fund_house' in scheme_perf.columns and 'aum_crore' in scheme_perf.columns:
        dist = scheme_perf.groupby('fund_house', as_index=False)['aum_crore'].sum()
        dist = dist.sort_values('aum_crore', ascending=False)
        dist['scheme_count'] = scheme_perf.groupby('fund_house')['scheme_name'].count().values
        return dist
    if 'fund_house' in scheme_perf.columns:
        return scheme_perf.groupby('fund_house', as_index=False)['scheme_name'].count().rename(columns={'scheme_name': 'scheme_count'})
    return pd.DataFrame()


def export_monthly_sip_trend(monthly_sip: pd.DataFrame) -> pd.DataFrame:
    if 'month' not in monthly_sip.columns:
        return pd.DataFrame()
    date_col = 'month'
    monthly_sip[date_col] = pd.to_datetime(monthly_sip[date_col], errors='coerce')
    return monthly_sip.sort_values(date_col)


def export_nav_trend(nav: pd.DataFrame, scheme_perf: pd.DataFrame) -> pd.DataFrame:
    if 'date' in nav.columns and 'nav' in nav.columns:
        if 'amfi_code' in nav.columns and 'amfi_code' in scheme_perf.columns:
            top_funds = scheme_perf.nlargest(5, 'aum_crore')[['amfi_code', 'scheme_name']].dropna()
            top_nav = nav[nav['amfi_code'].isin(top_funds['amfi_code'])].copy()
            top_nav = top_nav.merge(top_funds, on='amfi_code', how='left')
            top_nav['date'] = pd.to_datetime(top_nav['date'], errors='coerce')
            return top_nav.sort_values(['scheme_name', 'date'])
        else:
            return nav.copy()
    return pd.DataFrame()


def export_risk_return_scatter(scheme_perf: pd.DataFrame) -> pd.DataFrame:
    columns = [col for col in ['sharpe_ratio', 'std_dev_ann_pct', 'max_drawdown_pct', 'beta', 'alpha', 'aum_crore'] if col in scheme_perf.columns]
    if not columns:
        return pd.DataFrame()
    cols = ['scheme_name', 'fund_house', 'category'] + columns
    return scheme_perf[cols].copy()


def save_dashboard_dataframes(frames: dict[str, pd.DataFrame]) -> None:
    for name, df in frames.items():
        path = DASHBOARD_DATA_DIR / f'{name}.csv'
        df.to_csv(path, index=False)
        print(f'Saved dashboard data: {path}')


def create_placeholder_screenshot(filename: str, title: str) -> None:
    width, height = 1200, 700
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype('arial.ttf', 48)
    except Exception:
        font = ImageFont.load_default()
    text = title
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        text_width, text_height = font.getsize(text)
    x = (width - text_width) / 2
    y = (height - text_height) / 2
    draw.text((x, y), text, fill='black', font=font)
    path = SCREENSHOT_DIR / filename
    image.save(path, format='PNG')
    print(f'Saved screenshot placeholder: {path}')


def main() -> None:
    fund_master = load_dataframe(DATA_FILES['fund_master'])
    nav_history = load_dataframe(DATA_FILES['nav_history'])
    aum_by_fund_house = load_dataframe(DATA_FILES['aum_by_fund_house'])
    monthly_sip_inflows = load_dataframe(DATA_FILES['monthly_sip_inflows'])
    scheme_performance = load_dataframe(DATA_FILES['scheme_performance'])
    alpha_beta = load_dataframe(DATA_FILES['alpha_beta'])
    fund_scorecard = load_dataframe(DATA_FILES['fund_scorecard'])

    dashboard_frames = {
        'total_aum': compute_total_aum(scheme_performance, aum_by_fund_house),
        'average_nav': compute_average_nav(nav_history),
        'top_10_funds_by_aum': export_top_10_aum(scheme_performance),
        'cagr_comparison': export_cagr_comparison(scheme_performance),
        'sharpe_comparison': export_sharpe_comparison(scheme_performance),
        'fund_house_distribution': export_fund_house_distribution(scheme_performance),
        'monthly_sip_trend': export_monthly_sip_trend(monthly_sip_inflows),
        'nav_trend': export_nav_trend(nav_history, scheme_performance),
        'risk_return_scatter': export_risk_return_scatter(scheme_performance),
        'alpha_beta': alpha_beta,
        'fund_scorecard': fund_scorecard,
    }

    save_dashboard_dataframes(dashboard_frames)

    create_placeholder_screenshot('dashboard_overview.png', 'Dashboard Overview')
    create_placeholder_screenshot('top_10_funds_by_aum.png', 'Top 10 Funds by AUM')
    create_placeholder_screenshot('cagr_sharpe_scatter.png', 'CAGR vs Sharpe Comparison')
    create_placeholder_screenshot('alpha_beta_analysis.png', 'Alpha & Beta Analysis')
    create_placeholder_screenshot('nav_sip_trends.png', 'NAV Trend and SIP Trend')
    create_placeholder_screenshot('risk_return_scatter.png', 'Risk vs Return Scatter Plot')

    print('Dashboard data preparation complete.')


if __name__ == '__main__':
    main()
