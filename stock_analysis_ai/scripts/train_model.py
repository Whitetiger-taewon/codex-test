"""Train a simple RandomForest model for stock direction prediction."""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def find_processed_csv(processed_dir: Path) -> Path:
    """Return a processed CSV file path from the data/processed folder."""
    default_file = processed_dir / "processed_stock_data.csv"
    if default_file.exists():
        return default_file

    csv_files = sorted(processed_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(
            "No processed CSV file found in data/processed. "
            "Run preprocess.py first."
        )
    return csv_files[0]


def train_model() -> None:
    """Load data, train model, print accuracy, and save trained model."""
    # Set input/output paths.
    processed_dir = PROJECT_ROOT / "data" / "processed"
    model_path = PROJECT_ROOT / "models" / "stock_model.pkl"

    # Load processed data.
    csv_path = find_processed_csv(processed_dir)
    df = pd.read_csv(csv_path)

    # Support both requested feature names and preprocess.py names.
    # This keeps the script beginner-friendly and robust.
    column_aliases = {
        "MA5": ["MA5", "ma_5"],
        "MA20": ["MA20", "ma_20"],
        "Return": ["Return", "daily_return"],
        "Volume_Change": ["Volume_Change", "volume_change"],
        "target": ["target", "Target"],
    }

    selected_columns: dict[str, str] = {}
    for standard_name, options in column_aliases.items():
        found = next((name for name in options if name in df.columns), None)
        if found is None:
            raise ValueError(
                f"Missing required column for {standard_name}. "
                f"Expected one of: {options}"
            )
        selected_columns[standard_name] = found

    # Build feature matrix (X) and target vector (y).
    feature_columns = ["MA5", "MA20", "Return", "Volume_Change"]
    X = df[[selected_columns[name] for name in feature_columns]]
    y = df[selected_columns["target"]]

    # Split in time order (shuffle=False keeps earlier rows for training).
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        shuffle=False,
    )

    # Create and train the Random Forest classifier.
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate model accuracy on the test set.
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model accuracy: {accuracy:.4f}")

    # Save trained model to models/stock_model.pkl.
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    print(f"Model saved to: {model_path}")


if __name__ == "__main__":
    train_model()
