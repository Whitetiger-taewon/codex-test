"""Download stock price data from Yahoo Finance and save to CSV."""

from __future__ import annotations

import argparse
from pathlib import Path

import yfinance as yf


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download stock price data using yfinance and save it as a CSV file."
    )
    parser.add_argument("symbol", help="Ticker symbol to download (e.g., AAPL)")
    parser.add_argument(
        "--period",
        default="1y",
        help="Time period to download (default: 1y)",
    )
    parser.add_argument(
        "--interval",
        default="1d",
        help="Data interval to download (default: 1d)",
    )
    parser.add_argument(
        "--output-dir",
        default=Path(__file__).resolve().parents[1] / "data",
        type=Path,
        help="Directory where the CSV will be saved (default: stock_analysis_ai/data)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    data = yf.download(args.symbol, period=args.period, interval=args.interval, progress=False)
    if data.empty:
        raise ValueError(
            f"No data returned for symbol '{args.symbol}' with period '{args.period}' and interval '{args.interval}'."
        )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_file = args.output_dir / f"{args.symbol.upper()}_{args.period}_{args.interval}.csv"
    data.to_csv(output_file)

    print(f"Saved {len(data)} rows to {output_file}")


if __name__ == "__main__":
    main()
