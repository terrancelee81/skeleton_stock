import argparse
from forecaster.config.loader import load_config
from forecaster.services.pipeline import ForecastPipeline

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cfg", required=True, help="Path to YAML config")
    args = ap.parse_args()

    cfg = load_config(args.cfg)
    pipe = ForecastPipeline.from_config(cfg)
    results = pipe.run_backtest()
    print(results)

if __name__ == "__main__":
    main()
