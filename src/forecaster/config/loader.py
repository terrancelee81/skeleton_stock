from __future__ import annotations
import os
from typing import Any, Dict
import yaml
from .types import Config

def _read_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def _merge_dict(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge_dict(out[k], v)
        else:
            out[k] = v
    return out

def load_config(path: str) -> Config:
    # If you want hierarchical configs, detect and merge base.yaml here.
    cfg_dict = _read_yaml(path)
    base_path = os.path.join(os.path.dirname(path), "base.yaml")
    if os.path.exists(base_path) and os.path.abspath(base_path) != os.path.abspath(path):
        base_dict = _read_yaml(base_path)
        cfg_dict = _merge_dict(base_dict, cfg_dict)
    return Config(**cfg_dict)
