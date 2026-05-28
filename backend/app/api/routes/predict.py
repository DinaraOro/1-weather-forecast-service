from fastapi import APIRouter

from app.schemas.predict_schema import (
    PredictionRequest,
    PredictionResponse,
)

from app.services.prediction_service import (
    predict_temperature,
)


router = APIRouter()


@router.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict(
    request: PredictionRequest,
):

    forecast = predict_temperature(
        city=request.city,
        model_name=request.model_name,
        forecast_date=request.forecast_date,
    )

    return PredictionResponse(
        forecast=forecast,
    )