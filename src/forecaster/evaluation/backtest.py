from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Dict, List
from ..models.base import BaseModel

class WalkForwardBacktester:
    def __init__(self, train_size: int = 252*2, step: int = 20):
        self.train_size = train_size
        self.step = step

    def run(self, 
            df: pd.DataFrame, 
            feature_cols: List[str], 
            target_col: str,
            model: BaseModel,
            metrics: Dict[str, callable]) -> Dict[str, float]:

        preds, truths = [], []
        n = len(df)
        for start in range(0, n - self.train_size - self.step, self.step):
            train_idx = slice(start, start + self.train_size)
            test_idx  = slice(start + self.train_size, start + self.train_size + self.step)

            X_train = df.iloc[train_idx][feature_cols].values
            y_train = df.iloc[train_idx][target_col].values
            X_test  = df.iloc[test_idx][feature_cols].values
            y_test  = df.iloc[test_idx][target_col].values

            model.fit(X_train, y_train)
            y_hat = model.predict(X_test)

            preds.append(y_hat)
            truths.append(y_test)

        if preds and truths:
            y_pred = np.concatenate(preds)
            y_true = np.concatenate(truths)
        else:
            y_pred = np.array([])
            y_true = np.array([])

        return {name: fn(y_true, y_pred) for name, fn in metrics.items()}
