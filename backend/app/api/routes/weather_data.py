from fastapi import APIRouter

from app.data.storage import (
    load_raw_data,
)


router = APIRouter()


@router.get("/weather-data")
def get_weather_data(
    city: str,
):

    df = load_raw_data(
        city=city,
    )

    return df.to_dict(
        orient="records"
    )