"""Korean stock data collector using pykrx.

This module downloads daily OHLCV data for Korean stocks and saves it as
CSV files under ``stock_analysis_ai/data/raw``.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from pykrx import stock


RAW_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
DATE_FMT = "%Y%m%d"


def _default_date_range() -> tuple[str, str]:
    """Return a default 1-year date range in YYYYMMDD format."""
    end = datetime.today()
    start = end - timedelta(days=365)
    return start.strftime(DATE_FMT), end.strftime(DATE_FMT)


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
    print(f"CSV will be saved to: {output_path.resolve()}")
    data.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"CSV saved to: {output_path.resolve()}")
    print(f"Downloaded rows: {len(data)}")
    return output_path


if __name__ == "__main__":
    # Example: Samsung Electronics (005930)
    saved_file = collect_kr_stock_data("005930", start_date="20240101", end_date="20241231")
    print(f"Saved KR data to: {saved_file}")
