from __future__ import annotations
from typing import Dict, Any
from .sklearn import SklearnRegressor

def build_model(cfg: Dict[str, Any]):
    kind = cfg.get("kind", "sklearn.random_forest")
    params = cfg.get("params", {})
    if kind.startswith("sklearn"):
        # You can branch on specific sklearn models here.
        return SklearnRegressor()
    raise ValueError(f"Unknown model kind: {kind}")
