"""US stock data collector placeholder.

This file is prepared for future US stock data support.
Right now, it raises NotImplementedError on purpose.
"""

from __future__ import annotations


def collect_us_stock_data(*args, **kwargs):
    """Placeholder function for future US stock collection logic."""
    raise NotImplementedError(
        "US stock collection is not implemented yet. "
        "Add your yfinance or API logic here in the future."
    )


if __name__ == "__main__":
    # Simple message for beginners running this file directly.
    print("US collector is a placeholder and will be implemented later.")
