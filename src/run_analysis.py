import pandas as pd
from datetime import datetime

SECTORS = {
    "Technology": ["NVDA", "AAPL", "MSFT"],
    "Financial": ["JPM", "V", "BAC"],
    "Consumer Goods": ["WMT", "COST", "PG"]
}

BENCHMARK = "^GSPC"

def load_clean_data(sector, ticker):
    filepath = f"data/processed/{sector}/{ticker}_cleaned.csv"
    try:
        df = pd.read_csv(filepath)
        df['Date'] = pd.to_datetime(df["Date"], utc=True).dt.tz_localize(None)
        return df
    except Exception as e:
        print(f"Error loading cleaned data for {ticker}: {e}")
        return None
    
def summary_statistics(all_data, benchmark_data):
    summary = []

    benchmark_ret = None
    if benchmark_data is not None:
        benchmark_ret = benchmark_data['Daily_Percent_Return'].mean()

    for ticker, df in all_data.items():
        if df is None or df.empty:
            continue

        sector = "Benchmark" if ticker == BENCHMARK else next((s for s, tks in SECTORS.items() if ticker in tks), "Unknown")

        avg_return = df['Daily_Percent_Return'].mean()
        volatility = df['Daily_Percent_Return'].std()
        total_return = (df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0] * 100

        alpha = None
        if benchmark_ret is not None and ticker != BENCHMARK:
            alpha = avg_return - benchmark_ret

        summary.append({
            'Ticker': ticker,
            'Sector': sector,
            'Start_Date': df['Date'].min().date(),
            'End_Date': df['Date'].max().date(),
            'Start_Price': round(df['Close'].iloc[0], 2),
            'End_Price': round(df['Close'].iloc[-1], 2),
            'Daily_Return_%': round(avg_return, 4),
            'Volatility_%': round(volatility, 4),
            'Total_Return_%': round(total_return, 4),
            'Alpha_%': round(alpha, 4) if alpha is not None else None
        })

    return pd.DataFrame(summary)

def sector_performance(summary_df):
    stocks = summary_df[summary_df['Ticker'] != BENCHMARK].copy()

    if stocks.empty:
        return None
    
    sector_stats = stocks.groupby('Sector').agg({
        'Total_Return_%': 'mean',
        'Volatility_%': 'mean',
        'Daily_Return_%': 'mean',
        'Alpha_%': 'mean'
    }).round(4)

    sector_stats.columns = ['Avg_Total_Return_%', 'Avg_Volatility_%', 'Avg_Daily_Return_%', 'Avg_Alpha_%']

    sector_stats = sector_stats.sort_values(by='Avg_Total_Return_%', ascending=False).reset_index()


    return sector_stats

def calculate_correlations(all_data):
    price_data = {}

    for ticker, df in all_data.items():
        if df is not None and not df.empty:
            price_data[ticker] = df.set_index('Date')['Daily_Percent_Return']

    price_df = pd.DataFrame(price_data).dropna()

    correlation_matrix = price_df.corr().round(4)

    return correlation_matrix
    
def moving_average(all_data):
    ma_data = []

    for ticker, df in all_data.items():
        if df is None or df.empty or ticker == BENCHMARK:
            continue

        recent = df.iloc[-1]
        ma_50 = recent['MA_50']
        ma_200 = recent['MA_200']

        if pd.notna(ma_50) and pd.notna(ma_200):
            if ma_50 > ma_200:
                signal = "Bullish"
            else:
                signal = "Bearish"

            ma_data.append({
                'Ticker': ticker,
                'Current_Price': round(recent['Close'], 2),
                'MA_50': round(ma_50, 2),
                'MA_200': round(ma_200, 2),
                'Trend_Signal': signal
            })

    return pd.DataFrame(ma_data)

def volatility_analysis(all_data):
    vol_data = []

    for ticker, df in all_data.items():
        if df is None or df.empty:
            continue

        volatility = df['Daily_Percent_Return'].dropna()

        vol_data.append({
            'Ticker': ticker,
            'Mean_Return_%': round(volatility.mean(), 4),
            'Std_Dev_%': round(volatility.std(), 4),
            'Skewness': round(volatility.skew(), 4),
            'Kurtosis': round(volatility.kurtosis(), 4),
            'Min_Return_%': round(volatility.min(), 4),
            'Max_Return_%': round(volatility.max(), 4)
        })

    return pd.DataFrame(vol_data)

def main():
    all_data = {}

    benchmark_data = load_clean_data("Benchmark", BENCHMARK)

    if benchmark_data is not None:
        all_data[BENCHMARK] = benchmark_data

    for sector, tickers in SECTORS.items():
        for ticker in tickers:
            df = load_clean_data(sector, ticker)
            if df is not None:
                all_data[ticker] = df

    summary_df = summary_statistics(all_data, benchmark_data)
    summary_df.to_csv("results/data/summary_statistics.csv", index=False)

    sector_stats = sector_performance(summary_df)
    if sector_stats is not None:
        sector_stats.to_csv("results/data/sector_performance.csv", index=False)  

    ma_analysis = moving_average(all_data)
    ma_analysis.to_csv("results/data/moving_average_analysis.csv", index=False)

    correlation_matrix = calculate_correlations(all_data)
    correlation_matrix.to_csv("results/data/correlation_matrix.csv")

    volatility_stats = volatility_analysis(all_data)
    volatility_stats.to_csv("results/data/volatility_analysis.csv", index=False)

if __name__ == "__main__":
    main()
