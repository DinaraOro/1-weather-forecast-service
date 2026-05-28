from pydantic import BaseModel


class PredictionRequest(BaseModel):
    city: str
    model_name: str
    forecast_date: str


class ForecastItem(BaseModel):
    date: str
    prediction: float


class PredictionResponse(BaseModel):
    forecast: list[ForecastItem]