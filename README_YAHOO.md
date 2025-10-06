
# YahooDataSource Patch

## Files to copy into your repo
- `src/forecaster/data/yahoo.py`  (new)
- Update `src/forecaster/services/pipeline.py` imports and source switch block (see PIPELINE_PATCH.txt)
- `configs/aapl_yahoo.yaml` (example run config)

## Add dependency
Open `pyproject.toml` and add `yfinance` to dependencies:
```
dependencies = [
  "pandas>=2.1",
  "numpy>=1.24",
  "scikit-learn>=1.3",
  "pyyaml>=6.0",
  "joblib>=1.3",
  "matplotlib>=3.8",
  "yfinance>=0.2"
]
```

Then reinstall in editable mode:
```
pip install -e ".[dev]"
```

## Run
```
python scripts/backtest.py --cfg configs/aapl_yahoo.yaml
```
