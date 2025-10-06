from __future__ import annotations
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from .base import BaseModel

class SklearnRegressor(BaseModel):
    def __init__(self, model=None):
        self.model = model or RandomForestRegressor(n_estimators=200, random_state=42)

    def fit(self, X: np.ndarray, y: np.ndarray) -> "SklearnRegressor":
        self.model.fit(X, y)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)
