"""Build a small Korean stock universe CSV for beginner-friendly experiments.

This script creates a static list of 10 representative Korean stocks and saves
it as a CSV file under ``stock_analysis_ai/data/universe``.
"""

from __future__ import annotations

import csv
from pathlib import Path


# A beginner-friendly universe with well-known Korean companies.
# Tickers use the 6-digit KRX code format.
KR_STOCK_UNIVERSE = [
    {"ticker": "005930", "name": "Samsung Electronics", "market": "KOSPI"},
    {"ticker": "000660", "name": "SK hynix", "market": "KOSPI"},
    {"ticker": "035420", "name": "NAVER", "market": "KOSPI"},
    {"ticker": "005380", "name": "Hyundai Motor", "market": "KOSPI"},
    {"ticker": "051910", "name": "LG Chem", "market": "KOSPI"},
    {"ticker": "207940", "name": "Samsung Biologics", "market": "KOSPI"},
    {"ticker": "068270", "name": "Celltrion", "market": "KOSPI"},
    {"ticker": "035720", "name": "Kakao", "market": "KOSPI"},
    {"ticker": "066570", "name": "LG Electronics", "market": "KOSPI"},
    {"ticker": "091990", "name": "Celltrion Healthcare", "market": "KOSDAQ"},
]


def main() -> None:
    """Write the Korean stock universe to a CSV file."""
    project_root = Path(__file__).resolve().parents[1]
    output_file = project_root / "data" / "universe" / "kr_stock_universe.csv"

    # Create the folder if it does not exist yet.
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Write CSV with explicit column order: ticker, name, market.
    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["ticker", "name", "market"])
        writer.writeheader()
        writer.writerows(KR_STOCK_UNIVERSE)

    print(f"Saved {len(KR_STOCK_UNIVERSE)} stocks to {output_file}")


if __name__ == "__main__":
    main()
