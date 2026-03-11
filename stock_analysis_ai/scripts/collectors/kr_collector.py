"""Korean stock data collector using pykrx.

This module can:
1) Download daily OHLCV data for a single ticker.
2) Read a KR stock universe CSV file and download data for all tickers.

Each ticker is saved as its own CSV file under ``stock_analysis_ai/data/raw``.
"""

from __future__ import annotations

import csv
from datetime import datetime, timedelta
from pathlib import Path

from pykrx import stock


# Base folders used by this script.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
UNIVERSE_CSV_PATH = PROJECT_ROOT / "data" / "universe" / "kr_stock_universe.csv"

# Date format required by pykrx (YYYYMMDD).
DATE_FMT = "%Y%m%d"


def _default_date_range() -> tuple[str, str]:
    """Return a default 1-year date range in YYYYMMDD format."""
    end = datetime.today()
    start = end - timedelta(days=365)
    return start.strftime(DATE_FMT), end.strftime(DATE_FMT)


def load_kr_tickers_from_universe(universe_csv_path: Path = UNIVERSE_CSV_PATH) -> list[str]:
    """Read ticker codes from the Korean stock universe CSV file.

    Args:
        universe_csv_path: Path to ``kr_stock_universe.csv``.

    Returns:
        A list of ticker strings (for example: ["005930", "000660", ...]).
    """
    if not universe_csv_path.exists():
        raise FileNotFoundError(f"Universe CSV not found: {universe_csv_path}")

    tickers: list[str] = []

    # csv.DictReader reads rows like dictionaries using the header row.
    with universe_csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            ticker = (row.get("ticker") or "").strip()
            if ticker:
                tickers.append(ticker)

    if not tickers:
        raise ValueError(f"No tickers found in: {universe_csv_path}")

    return tickers


def collect_kr_stock_data(ticker: str, start_date: str | None = None, end_date: str | None = None) -> Path:
    """Download daily Korean stock OHLCV data and save to CSV.

    Args:
        ticker: Korean stock code (for example ``005930``).
        start_date: Start date in ``YYYYMMDD`` format. Defaults to 1 year ago.
        end_date: End date in ``YYYYMMDD`` format. Defaults to today.

    Returns:
        Path to the saved CSV file.
    """
    start, end = start_date, end_date
    if not start or not end:
        default_start, default_end = _default_date_range()
        start = start or default_start
        end = end or default_end

    data = stock.get_market_ohlcv_by_date(fromdate=start, todate=end, ticker=ticker)

    if data.empty:
        raise ValueError(f"No OHLCV data found for ticker '{ticker}' between {start} and {end}.")

    # Change Korean column names to simple English names.
    data = data.rename(
        columns={
            "시가": "Open",
            "고가": "High",
            "저가": "Low",
            "종가": "Close",
            "거래량": "Volume",
        }
    ).reset_index(names="Date")

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_path = RAW_DATA_DIR / f"{ticker}_{start}_{end}_1d.csv"
    data.to_csv(output_path, index=False, encoding="utf-8-sig")
    return output_path


def collect_all_kr_stock_data(start_date: str | None = None, end_date: str | None = None) -> None:
    """Download OHLCV data for all KR tickers in the universe CSV.

    This function prints progress for each ticker, skips failures, and continues.

    Args:
        start_date: Optional start date (YYYYMMDD). If omitted, defaults to 1 year ago.
        end_date: Optional end date (YYYYMMDD). If omitted, defaults to today.
    """
    tickers = load_kr_tickers_from_universe()

    start, end = start_date, end_date
    if not start or not end:
        default_start, default_end = _default_date_range()
        start = start or default_start
        end = end or default_end

    total = len(tickers)
    success_count = 0
    failed_tickers: list[str] = []

    print(f"[START] KR data collection for {total} tickers")
    print(f"Date range: {start} ~ {end}")
    print(f"Universe file: {UNIVERSE_CSV_PATH}")

    for index, ticker in enumerate(tickers, start=1):
        print(f"[{index}/{total}] Downloading {ticker}...")
        try:
            output_path = collect_kr_stock_data(ticker=ticker, start_date=start, end_date=end)
            success_count += 1
            print(f"[{index}/{total}] Done: {ticker} -> {output_path}")
        except Exception as error:  # noqa: BLE001 - beginner-friendly broad catch for batch jobs
            failed_tickers.append(ticker)
            print(f"[{index}/{total}] Skipped {ticker} (error: {error})")

    print("\n[SUMMARY]")
    print(f"Success: {success_count}")
    print(f"Failed: {len(failed_tickers)}")
    if failed_tickers:
        print("Failed tickers:", ", ".join(failed_tickers))


if __name__ == "__main__":
    # Run batch download for all tickers in the KR universe CSV.
    # Default date range is the last 1 year.
    collect_all_kr_stock_data()
