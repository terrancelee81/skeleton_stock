
from __future__ import annotations
import pandas as pd
from .interfaces import DataSource

class YahooDataSource(DataSource):
    """Fetch OHLCV from Yahoo Finance via yfinance.
    Returns a DataFrame indexed by Date with at least 'Adj Close'.
    """
    def __init__(self, interval: str = "1d", auto_adjust: bool = False):
        self.interval = interval
        self.auto_adjust = auto_adjust

    def load(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        try:
            import yfinance as yf
        except ImportError as e:
            raise ImportError(
                "yfinance is required for YahooDataSource. Install with: pip install yfinance"
            ) from e

        df = yf.download(
            tickers=ticker,
            start=start,
            end=end,
            interval=self.interval,
            auto_adjust=self.auto_adjust,
            progress=False,
            threads=True,
        )
        if df.empty:
            raise ValueError(f"No data returned from Yahoo for {ticker} between {start} and {end}")

        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
        df.index.name = "Date"
        df = df.sort_index()

        # yfinance columns: Open, High, Low, Close, Adj Close, Volume
        required_cols = {"Open","High","Low","Close","Adj Close","Volume"}
        missing = required_cols - set(df.columns)
        if missing:
            # If auto_adjust=True, 'Adj Close' may be missing: fallback to Close
            if "Adj Close" in missing and "Close" in df.columns:
                df["Adj Close"] = df["Close"]
                missing = missing - {"Adj Close"}
        if missing:
            raise ValueError(f"Missing columns from Yahoo response: {missing}")
        return df
