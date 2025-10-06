from __future__ import annotations
from dataclasses import asdict
from typing import Dict, List
import pandas as pd

from ..config.types import Config
from ..data.sources import CSVDataSource
from ..features.pipeline import FeaturePipeline
from ..features.transforms import Returns, SMA, Lag
from ..models.factory import build_model
from ..evaluation.backtest import WalkForwardBacktester
from ..evaluation import metrics as ev
from .logging import get_logger
from .registry import ArtifactRegistry

LOG = get_logger()

class ForecastPipeline:
    def __init__(self, cfg: Config):
        self.cfg = cfg

        data_cfg = cfg.data or {}
        src_kind = data_cfg.get("source", "csv")
        if src_kind == "csv":
            self.source = CSVDataSource(data_cfg.get("csv_path", "data/raw/AAPL.csv"))
        else:
            raise ValueError(f"Unknown data source: {src_kind}")

        self.model = build_model(cfg.model)

    @staticmethod
    def from_config(cfg: Config) -> "ForecastPipeline":
        return ForecastPipeline(cfg)

    def _build_features(self, df: pd.DataFrame) -> pd.DataFrame:
        steps = []
        for spec in self.cfg.features.get("transforms", []):
            t = spec.get("type")
            p = spec.get("params", {})
            if t == "Returns":
                steps.append(Returns())
            elif t == "SMA":
                steps.append(SMA(**p))
            elif t == "Lag":
                # Allow "Adj Close" key with spaces via dict access
                col = p.get("col", "Adj Close")
                lags = p.get("lags", 5)
                steps.append(Lag(col=col, lags=lags))
            else:
                raise ValueError(f"Unknown transform: {t}")
        fp = FeaturePipeline(steps)
        return fp.fit_transform(df)

    def run_backtest(self) -> Dict[str, float]:
        LOG.info("Loading data...")
        df_raw = self.source.load(
            ticker=self.cfg.data.get("ticker", "AAPL"),
            start=self.cfg.data.get("start", "2016-01-01"),
            end=self.cfg.data.get("end", "2025-01-01"),
        )
        LOG.info("Building features...")
        df = self._build_features(df_raw)

        target_col = self.cfg.target.get("column", "Adj Close")
        horizon = int(self.cfg.target.get("horizon", 1))
        df["__y__"] = df[target_col].shift(-horizon)
        df = df.dropna()

        feature_cols = [c for c in df.columns if c not in [target_col, "__y__"]]

        LOG.info("Starting walk-forward backtest...")
        bt = WalkForwardBacktester(
            train_size=int(self.cfg.backtest.get("train_size_days", 504)),
            step=int(self.cfg.backtest.get("step_days", 20)),
        )

        metric_map = {"MAE": ev.mae, "RMSE": ev.rmse, "MAPE": ev.mape, "DIR_ACC": ev.direction_acc}
        chosen = {k: metric_map[k] for k in self.cfg.metrics if k in metric_map}
        results = bt.run(df, feature_cols, "__y__", self.model, chosen)
        LOG.info("Backtest complete: %s", results)

        # Persist artifacts
        reg = ArtifactRegistry(self.cfg.paths.get("artifacts_dir", "artifacts"))
        run_dir = reg.save(self.cfg.run_name, self.model, results, asdict(self.cfg))
        LOG.info("Saved run artifacts to %s", run_dir)
        return results
