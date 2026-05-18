from pathlib import Path

import pandas as pd
import requests


CITY_COORDINATES = {
    "Amsterdam": {"latitude": 52.3676, "longitude": 4.9041},
    "London": {"latitude": 51.5072, "longitude": -0.1276},
    "Paris": {"latitude": 48.8566, "longitude": 2.3522},
    "Berlin": {"latitude": 52.5200, "longitude": 13.4050},
    "Moscow": {"latitude": 55.7558, "longitude": 37.6173},
}


def fetch_weather_history(
    city: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """
    Загружает исторические дневные погодные данные из Open-Meteo API.
    """

    if city not in CITY_COORDINATES:
        raise ValueError(f"Unknown city: {city}")

    coordinates = CITY_COORDINATES[city]

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"],
        "start_date": start_date,
        "end_date": end_date,
        "daily": [
            "temperature_2m_mean",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "wind_speed_10m_max",
        ],
        "timezone": "auto",
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data["daily"])
    df["city"] = city

    return df


def save_weather_history(
    city: str,
    start_date: str,
    end_date: str,
) -> Path:
    """
    Загружает данные и сохраняет их в data/raw/.
    """

    df = fetch_weather_history(
        city=city,
        start_date=start_date,
        end_date=end_date,
    )

    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{city.lower()}_{start_date}_{end_date}.csv"

    df.to_csv(output_path, index=False)

    return output_path


if __name__ == "__main__":
    path = save_weather_history(
        city="Amsterdam",
        start_date="2023-01-01",
        end_date="2024-12-31",
    )

    print(f"Saved weather data to: {path}")
