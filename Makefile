.PHONY: dev lint test fmt run-backtest

dev:
	python -m venv .venv && . .venv/bin/activate && pip install -e ".[dev]"

lint:
	ruff check src tests
	black --check src tests

fmt:
	black src tests
	ruff check --fix src tests

test:
	pytest -q

run-backtest:
	python scripts/backtest.py --cfg configs/aapl_daily.yaml
