"""Advanced analytics for Day 6 of the Bluestock Mutual Fund Analytics Capstone Project."""

from pathlib import Path
import warnings

import numpy as np
import pandas as pd

try:
    from scipy.stats import linregress
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False

try:
    import statsmodels.api as sm
    HAVE_STATSMODELS = True
except ImportError:
    HAVE_STATSMODELS = False

try:
    import matplotlib.pyplot as plt
    HAVE_MATPLOTLIB = True
except ImportError:
    HAVE_MATPLOTLIB = False

try:
    from PIL import Image, ImageDraw, ImageFont
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False

warnings.filterwarnings('ignore', category=UserWarning)

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / 'data' / 'raw'
PROCESSED_DIR = ROOT / 'data' / 'processed'
REPORTS_DIR = ROOT / 'reports'
CHARTS_DIR = REPORTS_DIR / 'advanced_charts'

REPORTS_DIR.mkdir(parents=True, exist_ok=True)
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

RISK_FREE_RATE = 0.065
TRADING_DAYS = 252
BENCHMARK_NAMES = ['Nifty 50', 'Nifty 100', 'Nifty Midcap 150', 'BSE SmallCap']

INPUT_FILES = {
    'fund_master': '01_fund_master.csv',
    'nav_history': '02_nav_history.csv',
    'scheme_performance': '07_scheme_performance.csv',
    'benchmark_indices': '10_benchmark_indices.csv',
}


def load_dataset(filename: str) -> pd.DataFrame:
    processed_path = PROCESSED_DIR / filename
    raw_path = RAW_DIR / filename
    if processed_path.exists():
        df = pd.read_csv(processed_path)
    elif raw_path.exists():
        df = pd.read_csv(raw_path)
    else:
        print(f'Warning: dataset not found: {filename}')
        return pd.DataFrame()
    df.columns = [str(col).strip().lower().replace(' ', '_') for col in df.columns]
    return df


def compute_daily_returns(nav_history: pd.DataFrame) -> pd.DataFrame:
    if nav_history.empty or 'nav' not in nav_history.columns or 'date' not in nav_history.columns:
        return pd.DataFrame(columns=['amfi_code', 'date', 'nav', 'daily_return'])
    nav = nav_history.copy()
    nav['date'] = pd.to_datetime(nav['date'], errors='coerce')
    nav = nav.sort_values(['amfi_code', 'date'])
    nav['daily_return'] = nav.groupby('amfi_code')['nav'].pct_change()
    return nav


def annualized_sharpe(returns: pd.Series) -> float:
    returns = returns.dropna()
    if returns.empty or returns.std() == 0:
        return np.nan
    mean_ann = returns.mean() * TRADING_DAYS
    std_ann = returns.std() * np.sqrt(TRADING_DAYS)
    return (mean_ann - RISK_FREE_RATE) / std_ann


def annualized_sortino(returns: pd.Series) -> float:
    returns = returns.dropna()
    downside = returns[returns < 0]
    if returns.empty or downside.empty:
        return np.nan
    mean_ann = returns.mean() * TRADING_DAYS
    downside_dev = np.sqrt((downside ** 2).mean()) * np.sqrt(TRADING_DAYS)
    if downside_dev == 0:
        return np.nan
    return (mean_ann - RISK_FREE_RATE) / downside_dev


def historic_var(returns: pd.Series, confidence_level: float = 0.95) -> float:
    returns = returns.dropna()
    if returns.empty:
        return np.nan
    percentile = 100 * (1 - confidence_level)
    var_value = -np.percentile(returns, percentile)
    return var_value


def max_drawdown(nav_history: pd.DataFrame) -> pd.DataFrame:
    if nav_history.empty or 'nav' not in nav_history.columns or 'date' not in nav_history.columns:
        return pd.DataFrame(columns=['amfi_code', 'max_drawdown', 'drawdown_start_date', 'drawdown_end_date'])
    results = []
    for amfi, group in nav_history.groupby('amfi_code'):
        group = group.sort_values('date').reset_index(drop=True)
        group['running_max'] = group['nav'].cummax()
        group['drawdown'] = 1 - group['nav'] / group['running_max']
        if group.empty:
            continue
        idx = group['drawdown'].idxmax()
        max_dd = group.loc[idx, 'drawdown']
        end_date = group.loc[idx, 'date']
        start_date = group.loc[:idx].loc[group['nav'].idxmax(), 'date']
        results.append({
            'amfi_code': amfi,
            'max_drawdown': max_dd,
            'drawdown_start_date': start_date,
            'drawdown_end_date': end_date,
        })
    return pd.DataFrame(results)


def compute_alpha_beta(nav_returns: pd.DataFrame, benchmark_indices: pd.DataFrame) -> pd.DataFrame:
    if nav_returns.empty or benchmark_indices.empty:
        return pd.DataFrame(columns=['amfi_code', 'benchmark', 'alpha', 'beta', 'tracking_error', 'r_squared'])
    benchmark_indices = benchmark_indices.copy()
    benchmark_indices['date'] = pd.to_datetime(benchmark_indices['date'], errors='coerce')
    benchmark_indices = benchmark_indices.sort_values(['index_name', 'date'])
    benchmark_indices['benchmark_return'] = benchmark_indices.groupby('index_name')['close_value'].pct_change()

    records = []
    for benchmark_name in BENCHMARK_NAMES:
        benchmark_df = benchmark_indices[benchmark_indices['index_name'].str.lower() == benchmark_name.lower()]
        if benchmark_df.empty:
            print(f'Warning: benchmark not found: {benchmark_name}')
            continue
        benchmark_df = benchmark_df[['date', 'benchmark_return']].dropna()

        merged = nav_returns.merge(benchmark_df, on='date', how='inner')
        for amfi, group in merged.groupby('amfi_code'):
            group = group.dropna(subset=['daily_return', 'benchmark_return'])
            if len(group) < 20:
                records.append({
                    'amfi_code': amfi,
                    'benchmark': benchmark_name,
                    'alpha': np.nan,
                    'beta': np.nan,
                    'tracking_error': np.nan,
                    'r_squared': np.nan,
                })
                continue
            x = group['benchmark_return'].values
            y = group['daily_return'].values
            if HAVE_STATSMODELS:
                x_with_const = sm.add_constant(x)
                model = sm.OLS(y, x_with_const).fit()
                alpha = float(model.params[0])
                beta = float(model.params[1])
                r_squared = float(model.rsquared)
            elif HAVE_SCIPY:
                slope, intercept, r_value, _, _ = linregress(x, y)
                alpha = float(intercept)
                beta = float(slope)
                r_squared = float(r_value ** 2)
            else:
                coeffs = np.polyfit(x, y, 1)
                beta = float(coeffs[0])
                alpha = float(coeffs[1])
                residuals = y - (beta * x + alpha)
                ss_res = np.sum(residuals ** 2)
                ss_tot = np.sum((y - np.mean(y)) ** 2)
                r_squared = float(1 - ss_res / ss_tot) if ss_tot != 0 else np.nan
            tracking_error = np.std(y - x) * np.sqrt(TRADING_DAYS)
            records.append({
                'amfi_code': amfi,
                'benchmark': benchmark_name,
                'alpha': alpha,
                'beta': beta,
                'tracking_error': tracking_error,
                'r_squared': r_squared,
            })
    return pd.DataFrame(records)


def build_sharpe_ranks(nav_returns: pd.DataFrame, fund_master: pd.DataFrame, scheme_performance: pd.DataFrame) -> pd.DataFrame:
    if nav_returns.empty:
        return pd.DataFrame(columns=['amfi_code', 'scheme_name', 'fund_house', 'sharpe_ratio', 'sortino_ratio', 'var_95', 'max_drawdown', 'sharpe_rank', 'sortino_rank', 'var_rank'])
    metrics = []
    drawdown_df = max_drawdown(nav_returns)
    for amfi, group in nav_returns.groupby('amfi_code'):
        returns = group['daily_return']
        metrics.append({
            'amfi_code': amfi,
            'sharpe_ratio': annualized_sharpe(returns),
            'sortino_ratio': annualized_sortino(returns),
            'var_95': historic_var(returns, 0.95),
        })
    metrics_df = pd.DataFrame(metrics)
    metrics_df = metrics_df.merge(drawdown_df, on='amfi_code', how='left')
    metadata = pd.DataFrame()
    if not scheme_performance.empty:
        metadata = scheme_performance[['amfi_code', 'scheme_name', 'fund_house']].drop_duplicates()
    elif not fund_master.empty:
        metadata = fund_master[['amfi_code', 'scheme_name', 'fund_house']].drop_duplicates()
    result = metrics_df.merge(metadata, on='amfi_code', how='left')
    result['sharpe_rank'] = result['sharpe_ratio'].rank(pct=True, ascending=False)
    result['sortino_rank'] = result['sortino_ratio'].rank(pct=True, ascending=False)
    result['var_rank'] = result['var_95'].rank(pct=True, ascending=True)
    return result[['amfi_code', 'scheme_name', 'fund_house', 'sharpe_ratio', 'sortino_ratio', 'var_95', 'max_drawdown', 'sharpe_rank', 'sortino_rank', 'var_rank']]


def build_var_drawdown_summary(nav_returns: pd.DataFrame) -> pd.DataFrame:
    if nav_returns.empty:
        return pd.DataFrame(columns=['amfi_code', 'var_95', 'max_drawdown', 'drawdown_start_date', 'drawdown_end_date'])
    metrics = []
    drawdown_df = max_drawdown(nav_returns)
    for amfi, group in nav_returns.groupby('amfi_code'):
        returns = group['daily_return']
        metrics.append({
            'amfi_code': amfi,
            'var_95': historic_var(returns, 0.95),
        })
    metrics_df = pd.DataFrame(metrics)
    return metrics_df.merge(drawdown_df, on='amfi_code', how='left')


def save_dataframe(df: pd.DataFrame, filename: str) -> None:
    path = REPORTS_DIR / filename
    df.to_csv(path, index=False)
    print(f'Saved {path}')


def create_placeholder_chart(filename: str, title: str) -> None:
    path = CHARTS_DIR / filename
    if HAVE_MATPLOTLIB:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, title, ha='center', va='center', fontsize=16, alpha=0.7)
        ax.set_axis_off()
        fig.savefig(path, dpi=180, bbox_inches='tight')
        plt.close(fig)
    elif HAVE_PIL:
        image = Image.new('RGB', (1200, 700), color='white')
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype('arial.ttf', 32)
        except Exception:
            font = ImageFont.load_default()
        try:
            bbox = draw.textbbox((0, 0), title, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
        except AttributeError:
            w, h = draw.textsize(title, font=font)
        draw.text(((1200 - w) / 2, (700 - h) / 2), title, fill='black', font=font)
        image.save(path)
    else:
        with open(path, 'wb') as f:
            f.write(b'')
    print(f'Saved chart placeholder: {path}')


def main() -> None:
    fund_master = load_dataset(INPUT_FILES['fund_master'])
    nav_history = load_dataset(INPUT_FILES['nav_history'])
    scheme_performance = load_dataset(INPUT_FILES['scheme_performance'])
    benchmark_indices = load_dataset(INPUT_FILES['benchmark_indices'])

    nav_returns = compute_daily_returns(nav_history)
    alpha_beta_df = compute_alpha_beta(nav_returns, benchmark_indices)
    sharpe_ranks_df = build_sharpe_ranks(nav_returns, fund_master, scheme_performance)
    var_drawdown_df = build_var_drawdown_summary(nav_returns)

    save_dataframe(alpha_beta_df, 'alpha_beta_table.csv')
    save_dataframe(sharpe_ranks_df, 'fund_sharpe_ranks.csv')
    save_dataframe(var_drawdown_df, 'var_drawdown_summary.csv')

    create_placeholder_chart('benchmark_comparison.png', 'Benchmark Comparison')
    create_placeholder_chart('risk_return_scatter.png', 'Risk vs Return Scatter Plot')
    create_placeholder_chart('alpha_beta_comparison.png', 'Alpha vs Beta Analysis')

    print('Advanced analytics pipeline complete.')


if __name__ == '__main__':
    main()
