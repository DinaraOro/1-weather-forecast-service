from pydantic import BaseModel


class ForecastRequest(BaseModel):

    lag_1: float
    lag_2: float
    lag_7: float

    rolling_mean_7: float

    precipitation: float

    wind: float