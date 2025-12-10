import yfinance as yf
import os
from datetime import datetime, timedelta
import time

SECTORS = {
    "Technology": ["NVDA", "AAPL", "MSFT"],
    "Financial": ["JPM", "V", "BAC"],
    "Consumer Goods": ["WMT", "COST", "PG"]
}

BENCHMARK = "^GSPC"

def fetch_stock_data(ticker, start_date, end_date):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        if data.empty:
            raise ValueError(f"No data found for ticker {ticker}")
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None
    
def save_raw_data(ticker, data, sector):
    directory = f"data/raw/{sector}"
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, f"{ticker}_raw.csv")
    data.to_csv(filepath)
    print(f"Saved raw data for {ticker} to {filepath}")

def main():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3*365) 

    benchmark_data = fetch_stock_data(BENCHMARK, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    if benchmark_data is not None:
        save_raw_data(BENCHMARK, benchmark_data, "Benchmark")

    for sector, tickers in SECTORS.items():
        for ticker in tickers:
            print(f"Fetching data for {ticker} in sector {sector}")
            data = fetch_stock_data(ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
            if data is not None:
                save_raw_data(ticker, data, sector)
            time.sleep(0.5)

if __name__ == "__main__":
    main()
