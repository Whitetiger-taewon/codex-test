"""Global stock collector router.

Use this module to choose the correct market collector by market code,
for example KR or US.
"""

from __future__ import annotations

from kr_collector import collect_kr_stock_data
from us_collector import collect_us_stock_data


def collect_stock_data(
    market_code: str,
    ticker: str,
    period: str = "1y",
    interval: str = "1d",
    start_date: str | None = None,
    end_date: str | None = None,
):
    """Collect stock data by market code.

    Args:
        market_code: Market identifier (KR, US, ...).
        ticker: Stock ticker/code.
        period: Download period (used by non-KR collectors).
        interval: Download interval (used by non-KR collectors).
        start_date: KR start date in YYYYMMDD.
        end_date: KR end date in YYYYMMDD.

    Returns:
        Path to saved CSV file for implemented markets.
    """
    code = market_code.strip().upper()

    if code == "KR":
        return collect_kr_stock_data(ticker=ticker, start_date=start_date, end_date=end_date)
    if code == "US":
        return collect_us_stock_data(ticker=ticker, period=period, interval=interval)

    raise ValueError(f"Unsupported market code: {market_code}. Use KR or US.")


if __name__ == "__main__":
    # Beginner-friendly example: route KR ticker to KR collector.
    result = collect_stock_data(market_code="KR", ticker="005930")
    print(f"Saved file: {result}")
