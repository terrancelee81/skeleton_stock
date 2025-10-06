from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class Config:
    run_name: str = "base_run"
    seed: int = 42
    paths: Dict[str, str] = field(default_factory=lambda: {"data_dir": "data", "artifacts_dir": "artifacts"})
    data: Dict[str, Any] = field(default_factory=dict)
    target: Dict[str, Any] = field(default_factory=lambda: {"column": "Adj Close", "horizon": 1})
    features: Dict[str, Any] = field(default_factory=lambda: {"transforms": []})
    model: Dict[str, Any] = field(default_factory=dict)
    backtest: Dict[str, Any] = field(default_factory=lambda: {"train_size_days": 504, "step_days": 20})
    metrics: List[str] = field(default_factory=lambda: ["MAE", "RMSE", "MAPE", "DIR_ACC"])
