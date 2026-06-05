"""Performance analytics module for Bluestock Mutual Fund Analytics Capstone."""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import linregress

sns.set_theme(style='whitegrid', font_scale=1.05)

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / 'data' / 'raw'
PROCESSED_DIR = ROOT / 'data' / 'processed'
REPORTS_DIR = ROOT / 'reports'
CHARTS_DIR = REPORTS_DIR / 'charts'
DB_DIR = ROOT / 'data' / 'db'

REPORTS_DIR.mkdir(parents=True, exist_ok=True)
CHARTS_DIR.mkdir(parents=True, exist_ok=True)
DB_DIR.mkdir(parents=True, exist_ok=True)

RISK_FREE_RATE = 0.065
TRADING_DAYS = 252

DATA_FILES = {
    'fund_master': '01_fund_master.csv',
    'nav_history': '02_nav_history.csv',
    'scheme_performance': '07_scheme_performance.csv',
    'investor_transactions': '08_investor_transactions.csv',
    'benchmark_indices': '10_benchmark_indices.csv',
}


def load_csv(name: str) -> pd.DataFrame:
    raw_path = RAW_DIR / DATA_FILES[name]
    processed_path = PROCESSED_DIR / DATA_FILES[name]
    if processed_path.exists():
        df = pd.read_csv(processed_path)
    elif raw_path.exists():
        df = pd.read_csv(raw_path)
    else:
        raise FileNotFoundError(f'Missing dataset: {DATA_FILES[name]}')
    df.columns = [str(col).strip().lower().replace(' ', '_') for col in df.columns]
    return df


def compute_daily_returns(nav: pd.DataFrame) -> pd.DataFrame:
    nav = nav.copy()
    nav['date'] = pd.to_datetime(nav['date'], errors='coerce')
    nav = nav.sort_values(['amfi_code', 'date'])
    nav['daily_return'] = nav.groupby('amfi_code')['nav'].pct_change()
    return nav


def compute_cagr_by_horizon(nav: pd.DataFrame, years: int) -> pd.DataFrame:
    nav = nav.copy()
    nav['date'] = pd.to_datetime(nav['date'], errors='coerce')
    results = []
    for amfi, group in nav.groupby('amfi_code'):
        group = group.sort_values('date')
        end_date = group['date'].max()
        start_date = end_date - pd.DateOffset(years=years)
        candidates = group.loc[group['date'] <= start_date]
        if candidates.empty or group['nav'].iat[0] <= 0:
            results.append({'amfi_code': amfi, f'cagr_{years}yr': np.nan})
            continue
        start_row = candidates.loc[candidates['date'].idxmax()]
        nav_start = start_row['nav']
        nav_end = group.loc[group['date'] == end_date, 'nav'].iloc[0]
        if nav_start <= 0 or nav_end <= 0:
            results.append({'amfi_code': amfi, f'cagr_{years}yr': np.nan})
            continue
        cagr = (nav_end / nav_start) ** (1 / years) - 1
        results.append({'amfi_code': amfi, f'cagr_{years}yr': cagr})
    return pd.DataFrame(results)


def annualize_sharpe(daily_returns: pd.Series) -> float:
    returns = daily_returns.dropna()
    if returns.empty or returns.std() == 0:
        return np.nan
    mean_ann = returns.mean() * TRADING_DAYS
    std_ann = returns.std() * np.sqrt(TRADING_DAYS)
    return (mean_ann - RISK_FREE_RATE) / std_ann


def annualize_sortino(daily_returns: pd.Series) -> float:
    returns = daily_returns.dropna()
    downside = returns[returns < 0]
    if returns.empty or downside.empty:
        return np.nan
    mean_ann = returns.mean() * TRADING_DAYS
    downside_dev = np.sqrt((downside ** 2).mean()) * np.sqrt(TRADING_DAYS)
    if downside_dev == 0:
        return np.nan
    return (mean_ann - RISK_FREE_RATE) / downside_dev


def compute_drawdown(nav_df: pd.DataFrame) -> pd.DataFrame:
    results = []
    for amfi, group in nav_df.groupby('amfi_code'):
        group = group.sort_values('date').reset_index(drop=True)
        group['running_max'] = group['nav'].cummax()
        group['drawdown'] = 1 - group['nav'] / group['running_max']
        if group['drawdown'].empty:
            results.append({
                'amfi_code': amfi,
                'max_drawdown': np.nan,
                'drawdown_start_date': pd.NaT,
                'drawdown_end_date': pd.NaT,
            })
            continue
        idx = group['drawdown'].idxmax()
        max_drawdown = group.loc[idx, 'drawdown']
        end_date = group.loc[idx, 'date']
        peak_window = group.loc[:idx]
        start_idx = peak_window['nav'].idxmax()
        start_date = group.loc[start_idx, 'date']
        results.append({
            'amfi_code': amfi,
            'max_drawdown': max_drawdown,
            'drawdown_start_date': start_date,
            'drawdown_end_date': end_date,
        })
    return pd.DataFrame(results)


def merge_benchmark_returns(nav_returns: pd.DataFrame, benchmark: pd.DataFrame, benchmark_name: str) -> pd.DataFrame:
    benchmark = benchmark.copy()
    benchmark['date'] = pd.to_datetime(benchmark['date'], errors='coerce')
    benchmark = benchmark[benchmark['index_name'].str.lower() == benchmark_name.lower()]
    benchmark = benchmark.sort_values('date')
    benchmark['benchmark_return'] = benchmark['close_value'].pct_change()
    return nav_returns.merge(benchmark[['date', 'benchmark_return']], on='date', how='left')


def compute_alpha_beta(nav_returns: pd.DataFrame, benchmark_returns: pd.DataFrame, benchmark_name: str) -> pd.DataFrame:
    merged = merge_benchmark_returns(nav_returns, benchmark_returns, benchmark_name)
    records = []
    for amfi, group in merged.groupby('amfi_code'):
        group = group.dropna(subset=['daily_return', 'benchmark_return'])
        if len(group) < 20:
            records.append({
                'amfi_code': amfi,
                'benchmark': benchmark_name,
                'alpha': np.nan,
                'beta': np.nan,
                'tracking_error': np.nan,
            })
            continue
        x = group['benchmark_return'].values
        y = group['daily_return'].values
        x_with_const = sm.add_constant(x)
        model = sm.OLS(y, x_with_const).fit()
        alpha = model.params[0]
        beta = model.params[1]
        tracking_error = np.std(y - x) * np.sqrt(TRADING_DAYS)
        records.append({
            'amfi_code': amfi,
            'benchmark': benchmark_name,
            'alpha': alpha,
            'beta': beta,
            'tracking_error': tracking_error,
        })
    return pd.DataFrame(records)


def build_scorecard(performance: pd.DataFrame, cagr: pd.DataFrame, stats: pd.DataFrame) -> pd.DataFrame:
    scorecard = performance.merge(cagr, on='amfi_code', how='left')
    scorecard = scorecard.merge(stats, on='amfi_code', how='left')
    scorecard['cagr_score'] = scorecard['cagr_3yr']
    scorecard['sharpe_score'] = scorecard['sharpe_ratio']
    scorecard['alpha_score'] = scorecard['alpha']
    scorecard['expense_score'] = scorecard['expense_ratio_pct']
    scorecard['drawdown_score'] = scorecard['max_drawdown']
    scorecard['cagr_rank'] = scorecard['cagr_score'].rank(pct=True, ascending=False)
    scorecard['sharpe_rank'] = scorecard['sharpe_score'].rank(pct=True, ascending=False)
    scorecard['alpha_rank'] = scorecard['alpha_score'].rank(pct=True, ascending=False)
    scorecard['expense_rank'] = 1 - scorecard['expense_score'].rank(pct=True, ascending=True)
    scorecard['drawdown_rank'] = 1 - scorecard['drawdown_score'].rank(pct=True, ascending=True)
    scorecard['fund_score'] = (
        0.30 * scorecard['cagr_rank']
        + 0.25 * scorecard['sharpe_rank']
        + 0.20 * scorecard['alpha_rank']
        + 0.15 * scorecard['expense_rank']
        + 0.10 * scorecard['drawdown_rank']
    )
    scorecard['rank'] = scorecard['fund_score'].rank(ascending=False, method='dense')
    scorecard = scorecard.sort_values(['rank', 'fund_score'], ascending=[True, False])
    return scorecard


def save_outputs(scorecard: pd.DataFrame, alpha_beta: pd.DataFrame, benchmark_df: pd.DataFrame) -> None:
    scorecard_path = REPORTS_DIR / 'fund_scorecard.csv'
    alpha_beta_path = REPORTS_DIR / 'alpha_beta.csv'
    benchmark_path = REPORTS_DIR / 'benchmark_comparison.csv'
    scorecard.to_csv(scorecard_path, index=False)
    alpha_beta.to_csv(alpha_beta_path, index=False)
    benchmark_df.to_csv(benchmark_path, index=False)
    print(f'Saved {scorecard_path}')
    print(f'Saved {alpha_beta_path}')
    print(f'Saved {benchmark_path}')


def create_benchmark_comparison_chart(benchmark_df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(14, 7))
    for fund_name, group in benchmark_df.groupby('scheme_name'):
        ax.plot(group['date'], group['fund_cumulative_return'], label=fund_name, linewidth=1.8)
    for benchmark_name, group in benchmark_df.groupby('benchmark_name'):
        ax.plot(group['date'], group['benchmark_cumulative_return'], label=benchmark_name, linestyle='--', linewidth=2)
    ax.set_title('Top 5 Fund Performance vs Benchmark Indices')
    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative Return')
    ax.legend(loc='best', fontsize='small')
    path = CHARTS_DIR / 'benchmark_comparison_chart.png'
    fig.savefig(path, dpi=220, bbox_inches='tight')
    print(f'Saved benchmark comparison chart: {path}')
    plt.close(fig)


def build_benchmark_comparison(top_funds: pd.DataFrame, nav_returns: pd.DataFrame, benchmark: pd.DataFrame) -> pd.DataFrame:
    benchmark = benchmark.copy()
    benchmark['date'] = pd.to_datetime(benchmark['date'], errors='coerce')
    benchmark = benchmark[benchmark['index_name'].isin(['Nifty 50', 'Nifty 100'])]
    benchmark = benchmark.sort_values('date')
    benchmark['benchmark_return'] = benchmark.groupby('index_name')['close_value'].pct_change()
    benchmark['benchmark_cumulative_return'] = (1 + benchmark['benchmark_return'].fillna(0)).groupby(benchmark['index_name']).cumprod() - 1

    results = []
    for _, row in top_funds.iterrows():
        amfi = row['amfi_code']
        scheme_name = row['scheme_name']
        fund_nav = nav_returns[nav_returns['amfi_code'] == amfi].copy()
        fund_nav['fund_cumulative_return'] = (1 + fund_nav['daily_return'].fillna(0)).cumprod() - 1
        for benchmark_name in ['Nifty 50', 'Nifty 100']:
            bench = benchmark[benchmark['index_name'] == benchmark_name][['date', 'benchmark_return', 'benchmark_cumulative_return']]
            merged = fund_nav.merge(bench, on='date', how='inner')
            merged['scheme_name'] = scheme_name
            merged['benchmark_name'] = benchmark_name
            results.append(merged[['date', 'scheme_name', 'benchmark_name', 'fund_cumulative_return', 'benchmark_cumulative_return']])
    if not results:
        return pd.DataFrame()
    return pd.concat(results, ignore_index=True)


def main() -> None:
    fund_master = load_csv('fund_master')
    nav_history = load_csv('nav_history')
    scheme_performance = load_csv('scheme_performance')
    benchmark_indices = load_csv('benchmark_indices')

    nav_returns = compute_daily_returns(nav_history)
    cagr_1 = compute_cagr_by_horizon(nav_history, 1)
    cagr_3 = compute_cagr_by_horizon(nav_history, 3)
    cagr_5 = compute_cagr_by_horizon(nav_history, 5)
    cagr = cagr_1.merge(cagr_3, on='amfi_code', how='outer').merge(cagr_5, on='amfi_code', how='outer')

    returns_summary = (
        nav_returns.groupby('amfi_code')['daily_return']
        .apply(lambda series: pd.Series({
            'sharpe_ratio': annualize_sharpe(series),
            'sortino_ratio': annualize_sortino(series),
        }))
        .reset_index()
    )

    drawdown_df = compute_drawdown(nav_history)
    merged_stats = returns_summary.merge(drawdown_df, on='amfi_code', how='left')

    alpha_beta_nifty50 = compute_alpha_beta(nav_returns, benchmark_indices, 'Nifty 50')
    alpha_beta_nifty100 = compute_alpha_beta(nav_returns, benchmark_indices, 'Nifty 100')
    alpha_beta = pd.concat([alpha_beta_nifty50, alpha_beta_nifty100], ignore_index=True)

    performance_stats = scheme_performance.copy()
    scorecard = build_scorecard(performance_stats, cagr, merged_stats)

    top5 = scorecard.head(5)
    benchmark_comparison_df = build_benchmark_comparison(top5, nav_returns, benchmark_indices)
    if not benchmark_comparison_df.empty:
        create_benchmark_comparison_chart(benchmark_comparison_df)

    save_outputs(scorecard, alpha_beta, benchmark_comparison_df)

    print('Performance analytics pipeline completed.')


if __name__ == '__main__':
    main()
