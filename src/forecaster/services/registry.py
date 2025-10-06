from __future__ import annotations
import os, json, joblib
from datetime import datetime

class ArtifactRegistry:
    def __init__(self, artifacts_dir: str):
        self.artifacts_dir = artifacts_dir
        os.makedirs(self.artifacts_dir, exist_ok=True)

    def _run_dir(self, run_name: str) -> str:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        d = os.path.join(self.artifacts_dir, f"{run_name}_{ts}")
        os.makedirs(d, exist_ok=True)
        return d

    def save(self, run_name: str, model, metrics: dict, config: dict) -> str:
        d = self._run_dir(run_name)
        joblib.dump(model, os.path.join(d, "model.joblib"))
        with open(os.path.join(d, "metrics.json"), "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)
        with open(os.path.join(d, "config.json"), "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        return d
