from fastapi import FastAPI

from backend.app.schemas.forecast_schema import (
    ForecastRequest,
)

from backend.app.services.forecast_service import (
    predict_temperature,
)

app = FastAPI()


@app.get("/")
def root():

    return {
        "message": "Weather Forecast Service is running"
    }


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.post("/predict")
def predict(request: ForecastRequest):

    try:

        prediction = predict_temperature(request)

        return {
            "prediction": prediction
        }

    except Exception as e:

        return {
            "error": str(e)
        }