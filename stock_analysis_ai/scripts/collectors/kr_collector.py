"""Korean stock data collector.

This module downloads Korean stock data and saves it as a CSV file in the
project data folder.
"""

from __future__ import annotations

from pathlib import Path

import yfinance as yf


# Project-level data folder: stock_analysis_ai/data
DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def _format_kr_ticker(ticker: str, market_suffix: str = "KS") -> str:
    """Format a Korean ticker for Yahoo Finance.

    Example:
        005930 -> 005930.KS
    """
    cleaned = ticker.strip().upper()
    if "." in cleaned:
        return cleaned
    return f"{cleaned}.{market_suffix}"


def collect_kr_stock_data(
    ticker: str,
    period: str = "1y",
    interval: str = "1d",
    market_suffix: str = "KS",
) -> Path:
    """Download Korean stock data and save it to a CSV file.

    Args:
        ticker: Korean stock code (for example: 005930).
        period: Data period for yfinance (default: 1y).
        interval: Data interval for yfinance (default: 1d).
        market_suffix: Yahoo Finance market suffix (KS for KOSPI, KQ for KOSDAQ).

    Returns:
        Path to the saved CSV file.
    """
    yahoo_ticker = _format_kr_ticker(ticker, market_suffix=market_suffix)
    data = yf.download(yahoo_ticker, period=period, interval=interval, progress=False)

    if data.empty:
        raise ValueError(f"No data found for ticker '{yahoo_ticker}'.")

    # Make sure the data folder exists before saving.
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_path = DATA_DIR / f"{yahoo_ticker}_{period}_{interval}.csv"
    data.to_csv(output_path)
    return output_path


if __name__ == "__main__":
    # Beginner-friendly example run.
    saved_file = collect_kr_stock_data("005930")
    print(f"Saved KR data to: {saved_file}")
