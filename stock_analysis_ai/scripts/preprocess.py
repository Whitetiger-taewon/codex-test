"""Preprocess raw stock data into a feature-ready dataset."""

from pathlib import Path
import argparse

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def preprocess_data(input_path: Path, output_path: Path) -> None:
    """Load raw CSV data, create features/target, and save processed data."""
    # Load raw stock data from CSV.
    df = pd.read_csv(input_path)

    # Sort by date so rolling features and target are calculated correctly.
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")

    # Create simple technical features.
    df["ma_5"] = df["Close"].rolling(window=5).mean()
    df["ma_20"] = df["Close"].rolling(window=20).mean()
    df["daily_return"] = df["Close"].pct_change()
    df["volume_change"] = df["Volume"].pct_change()

    # Create target:
    # 1 if next day's close is higher than today's close, else 0.
    df["target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

    # Remove rows with missing values caused by rolling windows/shift.
    df = df.dropna().reset_index(drop=True)

    # Make sure the output folder exists, then save processed data.
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Processed data saved to: {output_path}")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for input and output file paths."""
    parser = argparse.ArgumentParser(description="Preprocess stock CSV data")
    parser.add_argument(
        "--input",
        type=Path,
        default=PROJECT_ROOT / "data" / "raw" / "stock_data.csv",
        help="Path to raw CSV file (default: stock_analysis_ai/data/raw/stock_data.csv)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "data" / "processed" / "processed_stock_data.csv",
        help="Path to save processed CSV (default: stock_analysis_ai/data/processed/processed_stock_data.csv)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Input file not found: {args.input}")

    preprocess_data(args.input, args.output)


if __name__ == "__main__":
    main()
