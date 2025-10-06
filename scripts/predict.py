import argparse
import pandas as pd
from forecaster.config.loader import load_config
from forecaster.services.pipeline import ForecastPipeline

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cfg", required=True)
    args = ap.parse_args()

    cfg = load_config(args.cfg)
    pipe = ForecastPipeline.from_config(cfg)
    # NOTE: This just runs backtest and prints last prediction.
    # Extend to load a saved model and run true out-of-sample predictions.
    preds = pipe.run_backtest()
    print(preds)

if __name__ == "__main__":
    main()
