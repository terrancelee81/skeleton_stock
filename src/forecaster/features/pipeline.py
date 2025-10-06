from __future__ import annotations
from typing import List
import pandas as pd
from .base import Transformer

class FeaturePipeline:
    def __init__(self, steps: List[Transformer]):
        self.steps = steps

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        for step in self.steps:
            step.fit(df)
            df = step.transform(df)
        return df
