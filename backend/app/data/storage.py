from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[3]

RAW_DATA_DIR = BASE_DIR / "data" / "raw"


def save_raw_data(
    df: pd.DataFrame,
    city: str,
    start_date: str,
    end_date: str,
):

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    filename = (
        f"{city.lower()}_"
        f"{start_date}_{end_date}.csv"
    )

    filepath = RAW_DATA_DIR / filename

    df.to_csv(
        filepath,
        index=False,
    )

    print(f"Saved data to: {filepath}")


def load_raw_data(
    city: str,
):

    city = city.lower()

    files = list(
        RAW_DATA_DIR.glob(
            f"{city}_*.csv"
        )
    )

    if not files:

        raise FileNotFoundError(
            f"No dataset found for city: {city}"
        )

    latest_file = max(
        files,
        key=lambda f: f.stat().st_mtime,
    )

    print(f"Loading dataset: {latest_file}")

    df = pd.read_csv(latest_file)

    return df