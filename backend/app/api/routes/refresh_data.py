from fastapi import APIRouter

from app.services.data_refresh_service import (
    refresh_weather_data,
)


router = APIRouter()


@router.post("/refresh-data")
def refresh_data(
    city: str,
):

    result = refresh_weather_data(
        city=city,
    )

    return result