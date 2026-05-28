import requests
import pandas as pd

from app.data.storage import save_raw_data


def get_coordinates(city: str):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    response = requests.get(
        url,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    results = data.get("results")

    if not results:
        raise ValueError(
            f"City not found: {city}"
        )

    latitude = results[0]["latitude"]
    longitude = results[0]["longitude"]

    return latitude, longitude


def load_weather_data(
    city: str,
    start_date: str,
    end_date: str,
):

    latitude, longitude = get_coordinates(city)

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
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

    response = requests.get(
        url,
        params=params,
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    daily_data = data["daily"]

    df = pd.DataFrame(
        {
            "date": daily_data["time"],
            "temperature": daily_data["temperature_2m_mean"],
            "temperature_2m_max": daily_data["temperature_2m_max"],
            "temperature_2m_min": daily_data["temperature_2m_min"],
            "precipitation": daily_data["precipitation_sum"],
            "wind_speed": daily_data["wind_speed_10m_max"],
            "city": city,
        }
    )

    return df


def save_weather_history(
    city: str,
    start_date: str,
    end_date: str,
):

    df = load_weather_data(
        city=city,
        start_date=start_date,
        end_date=end_date,
    )

    save_raw_data(
        df=df,
        city=city,
        start_date=start_date,
        end_date=end_date,
    )

    return df