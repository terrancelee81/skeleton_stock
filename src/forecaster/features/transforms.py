from __future__ import annotations
import pandas as pd
from .base import Transformer

class Returns(Transformer):
    def fit(self, df: pd.DataFrame) -> "Returns":
        return self
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["ret_1d"] = df["Adj Close"].pct_change()
        return df

class SMA(Transformer):
    def __init__(self, window: int = 10):
        self.window = window
    def fit(self, df: pd.DataFrame) -> "SMA":
        return self
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df[f"sma_{self.window}"] = df["Adj Close"].rolling(self.window).mean()
        return df

class Lag(Transformer):
    def __init__(self, col: str, lags: int = 5):
        self.col, self.lags = col, lags
    def fit(self, df: pd.DataFrame) -> "Lag":
        return self
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for i in range(1, self.lags + 1):
            df[f"{self.col}_lag{i}"] = df[self.col].shift(i)
        return df
