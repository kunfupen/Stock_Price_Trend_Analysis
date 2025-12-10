import pandas as pd
import os

SECTORS = {
    "Technology": ["NVDA", "AAPL", "MSFT"],
    "Financial": ["JPM", "V", "BAC"],
    "Consumer Goods": ["WMT", "COST", "PG"]
}

BENCHMARK = "^GSPC"

def create_directories():
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('data/processed/Benchmark', exist_ok=True)
    for sector in SECTORS.keys():
        os.makedirs(f'data/processed/{sector}', exist_ok=True)

def load_raw_data(sector, ticker):
    filepath = f"data/raw/{sector}/{ticker}_raw.csv"
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"Raw data file not found for {ticker} in sector {sector}")
        return None
    except Exception as e:
        print(f"Error loading data for {ticker}: {e}")
        return None

def clean_stock_data(df, ticker):
    if df is None or df.empty:
        return None
    
    cleaned_df = df.copy()
    cleaned_df['Date'] = pd.to_datetime(cleaned_df["Date"], utc=True).dt.tz_localize(None)

    cleaned_df.sort_values(by='Date', inplace=True)

    cleaned_df.drop_duplicates(subset='Date', keep='first', inplace=True)   

    crit_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    cleaned_df.dropna(subset=crit_cols, inplace=True)

    cleaned_df = cleaned_df[(cleaned_df['Volume'] > 0) & (cleaned_df['Close'] > 0)]

    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna().bfill()

    cleaned_df['Daily_Percent_Return'] = cleaned_df['Close'].pct_change() * 100

    cleaned_df['MA_50'] = cleaned_df['Close'].rolling(window=50, min_periods=1).mean()

    cleaned_df['MA_200'] = cleaned_df['Close'].rolling(window=200, min_periods=1).mean()

    cleaned_df['Ticker'] = ticker

    cleaned_df['Open'] = cleaned_df['Open'].round(2)
    cleaned_df['High'] = cleaned_df['High'].round(2)
    cleaned_df['Low'] = cleaned_df['Low'].round(2)
    cleaned_df['Close'] = cleaned_df['Close'].round(2)
    cleaned_df['Daily_Percent_Return'] = cleaned_df['Daily_Percent_Return'].round(4)
    cleaned_df['MA_50'] = cleaned_df['MA_50'].round(2)
    cleaned_df['MA_200'] = cleaned_df['MA_200'].round(2)

    column_order = ['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume', 
                    'Daily_Percent_Return', 'MA_50', 'MA_200', 'Dividends', 'Stock Splits']
    
    cleaned_df = cleaned_df[column_order]
    cleaned_df.reset_index(drop=True, inplace=True)
    return cleaned_df

def save_cleaned_data(df, ticker, sector):
    if df is None or df.empty:
        return
    
    csv_filepath = f"data/processed/{sector}/{ticker}_cleaned.csv"
    df.to_csv(csv_filepath, index=False)


def main():
    create_directories()

    benchmark_df = load_raw_data("Benchmark", BENCHMARK)

    if benchmark_df is not None:
        cleaned_benchmark_df = clean_stock_data(benchmark_df, "Benchmark")
        if cleaned_benchmark_df is not None:
            save_cleaned_data(cleaned_benchmark_df, BENCHMARK, "Benchmark")

    for sector, tickers in SECTORS.items():
        for ticker in tickers:
            print(f"Cleaning data for {ticker} in sector {sector}")
            raw_df = load_raw_data(sector, ticker)
            if raw_df is not None:
                cleaned_df = clean_stock_data(raw_df, ticker)
                if cleaned_df is not None:
                    save_cleaned_data(cleaned_df, ticker, sector)

if __name__ == "__main__":
    main()