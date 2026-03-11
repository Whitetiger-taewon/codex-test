"""Predict next-day stock movement using the latest processed data row."""

from pathlib import Path

import joblib
import pandas as pd


def find_latest_file(folder: Path, pattern: str) -> Path:
    """Return the most recently modified file that matches a pattern."""
    files = list(folder.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No files matching '{pattern}' found in {folder}")
    return max(files, key=lambda file_path: file_path.stat().st_mtime)


def predict_next_day() -> None:
    """Load model + latest processed row and print UP or DOWN prediction."""
    # Paths used by the project.
    models_dir = Path("models")
    processed_dir = Path("data/processed")

    # Find the newest trained model and newest processed CSV file.
    model_path = find_latest_file(models_dir, "*.pkl")
    processed_path = find_latest_file(processed_dir, "*.csv")

    # Load model and processed dataset.
    model = joblib.load(model_path)
    df = pd.read_csv(processed_path)

    if df.empty:
        raise ValueError(f"Processed file is empty: {processed_path}")

    # Support both naming styles used in this project.
    column_aliases = {
        "MA5": ["MA5", "ma_5"],
        "MA20": ["MA20", "ma_20"],
        "Return": ["Return", "daily_return"],
        "Volume_Change": ["Volume_Change", "volume_change"],
    }

    selected_columns: list[str] = []
    for standard_name, options in column_aliases.items():
        found = next((name for name in options if name in df.columns), None)
        if found is None:
            raise ValueError(
                f"Missing required column for {standard_name}. Expected one of: {options}"
            )
        selected_columns.append(found)

    # Use the latest row only (most recent data point) for prediction.
    latest_features = df[selected_columns].tail(1)

    # Predict next-day movement: 1 = UP, 0 = DOWN.
    prediction = model.predict(latest_features)[0]
    direction = "UP" if int(prediction) == 1 else "DOWN"

    print(f"Model file: {model_path}")
    print(f"Data file: {processed_path}")
    print(f"Predicted next-day movement: {direction}")


if __name__ == "__main__":
    predict_next_day()
