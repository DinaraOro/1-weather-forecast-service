from datetime import datetime, timedelta

import pandas as pd

from app.data.storage import (
    load_raw_data,
    save_raw_data,
)

from app.data.weather_loader import (
    load_weather_data,
)


def refresh_weather_data(
    city: str,
):

    # Load latest dataset
    existing_df = load_raw_data(
        city=city,
    )

    existing_df["date"] = pd.to_datetime(
        existing_df["date"]
    )

    # Find last available date
    latest_date = (
        existing_df["date"]
        .max()
    )

    # Next missing day
    start_date = (
        latest_date
        + timedelta(days=1)
    )

    # Today
    end_date = datetime.today()

    # Nothing to update
    if start_date.date() > end_date.date():

        return {
            "message": "Dataset already up to date"
        }

    # Download new data
    new_df = load_weather_data(
        city=city,
        start_date=str(start_date.date()),
        end_date=str(end_date.date()),
    )

    new_df["date"] = pd.to_datetime(
        new_df["date"]
    )

    # Merge datasets
    updated_df = pd.concat(
        [
            existing_df,
            new_df,
        ]
    )

    updated_df = (
        updated_df
        .drop_duplicates(
            subset=["date"]
        )
        .sort_values("date")
    )

    # Save new latest dataset
    save_raw_data(
        df=updated_df,
        city=city,
        start_date=str(
            updated_df["date"]
            .min()
            .date()
        ),
        end_date=str(
            updated_df["date"]
            .max()
            .date()
        ),
    )

    return {
        "message": "Weather data updated",
        "new_rows": len(new_df),
        "latest_date": str(
            updated_df["date"]
            .max()
            .date()
        ),
    }