from app.data.fetch_weather import (
    save_weather_history,
)


cities = [
    "Lisbon",
    "Amsterdam",
    "Berlin",
    "Paris",
]


for city in cities:

    path = save_weather_history(
        city=city,
        start_date="2023-01-01",
        end_date="2026-05-15",
    )

    print(f"Saved weather data to: {path}")