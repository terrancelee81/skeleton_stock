from __future__ import annotations
from abc import ABC, abstractmethod
import pandas as pd

class Transformer(ABC):
    @abstractmethod
    def fit(self, df: pd.DataFrame) -> "Transformer":
        return self

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError
