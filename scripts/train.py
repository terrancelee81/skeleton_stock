import argparse
from forecaster.config.loader import load_config
from forecaster.services.pipeline import ForecastPipeline

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cfg", required=True)
    args = ap.parse_args()

    cfg = load_config(args.cfg)
    pipe = ForecastPipeline.from_config(cfg)
    metrics = pipe.run_backtest()  # simple placeholder "train"
    print("Training/backtest metrics:", metrics)

if __name__ == "__main__":
    main()
