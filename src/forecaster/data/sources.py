from __future__ import annotations
import pandas as pd
from .interfaces import DataSource

class CSVDataSource(DataSource):
    """Load a single-ticker CSV with a 'Date' column and OHLCV columns.
    Extend or add new classes for different schemas or APIs.
    """
    def __init__(self, path: str):
        self.path = path

    def load(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        df = pd.read_csv(self.path, parse_dates=["Date"]).set_index("Date").sort_index()
        return df.loc[start:end]
