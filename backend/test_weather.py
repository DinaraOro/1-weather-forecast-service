from app.services.training_service import (
    train_model,
)

from app.services.prediction_service import (
    predict_temperature,
)


CITY = "Lisbon"

START_DATE = "2023-01-01"

END_DATE = "2025-05-01"

MODEL_NAME = "arima"


metrics = train_model(
    model_name=MODEL_NAME,
    city=CITY,
    start_date=START_DATE,
    end_date=END_DATE,
)

print("Training metrics:")

print(metrics)


prediction = predict_temperature(
    model_name=MODEL_NAME,
    city=CITY,
    start_date=START_DATE,
    end_date=END_DATE,
)

print(f"Next day prediction: {prediction:.2f} °C")