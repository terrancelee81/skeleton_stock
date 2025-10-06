from __future__ import annotations
from abc import ABC, abstractmethod
import pandas as pd

class DataSource(ABC):
    @abstractmethod
    def load(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        """Return OHLCV DataFrame indexed by datetime with at least 'Adj Close' column."""
        raise NotImplementedError
