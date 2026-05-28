import joblib
import pandas as pd

from datetime import timedelta

from app.data.storage import (
    load_raw_data,
)

from app.models.lstm_model import (
    LSTMWeatherModel,
)

from app.models.arima_model import (
    ARIMAModel,
)


FORECAST_HORIZON = 7


def predict_temperature(
    city: str,
    model_name: str,
    forecast_date: str,
):

    city = city.lower()

    # Load latest available dataset
    df = load_raw_data(
        city=city,
    )

    df["date"] = pd.to_datetime(
        df["date"]
    )

    forecast_start = pd.to_datetime(
        forecast_date
    )

    history = (
        df[df["date"] < forecast_start]
        .sort_values("date")
        .copy()
    )

    if len(history) < 7:

        raise ValueError(
            "Not enough historical data before forecast date"
        )

    # =========================
    # RANDOM FOREST
    # =========================

    if model_name == "random_forest":

        model_path = (
            f"/app/artifacts/"
            f"{model_name}.pkl"
        )

        model = joblib.load(
            model_path
        )

        forecast = []

        temperatures = (
            history["temperature"]
            .tolist()
        )

        for step in range(
            FORECAST_HORIZON
        ):

            current_forecast_date = (
                forecast_start
                + timedelta(days=step)
            )

            features = pd.DataFrame(
                {
                    "lag_1": [
                        temperatures[-1]
                    ],

                    "lag_2": [
                        temperatures[-2]
                    ],

                    "lag_7": [
                        temperatures[-7]
                    ],

                    "rolling_mean_3": [
                        sum(
                            temperatures[-3:]
                        ) / 3
                    ],

                    "rolling_mean_7": [
                        sum(
                            temperatures[-7:]
                        ) / 7
                    ],

                    "month": [
                        current_forecast_date.month
                    ],

                    "weekday": [
                        current_forecast_date.weekday()
                    ],

                    "day_of_year": [
                        current_forecast_date.dayofyear
                    ],
                }
            )

            prediction = model.predict(
                features
            )[0]

            prediction = float(
                prediction
            )

            forecast.append(
                {
                    "date": str(
                        current_forecast_date.date()
                    ),
                    "prediction": prediction,
                }
            )

            temperatures.append(
                prediction
            )

        return forecast

    # =========================
    # LSTM
    # =========================

    elif model_name == "lstm":

        model = LSTMWeatherModel()

        model.load()

        temperatures = (
            history["temperature"]
            .tolist()
        )

        forecast = []

        for step in range(
            FORECAST_HORIZON
        ):

            current_forecast_date = (
                forecast_start
                + timedelta(days=step)
            )

            latest_sequence = (
                temperatures[-7:]
            )

            prediction = (
                model.predict_next(
                    latest_sequence
                )
            )

            forecast.append(
                {
                    "date": str(
                        current_forecast_date.date()
                    ),
                    "prediction": prediction,
                }
            )

            temperatures.append(
                prediction
            )

        return forecast

    # =========================
    # ARIMA
    # =========================

    elif model_name == "arima":

        model = ARIMAModel()

        model.load()

        predictions = model.predict(
            steps=FORECAST_HORIZON
        )

        forecast = []

        for step in range(
            FORECAST_HORIZON
        ):

            current_forecast_date = (
                forecast_start
                + timedelta(days=step)
            )

            forecast.append(
                {
                    "date": str(
                        current_forecast_date.date()
                    ),
                    "prediction": float(
                        predictions[step]
                    ),
                }
            )

        return forecast

    else:

        raise ValueError(
            f"Unsupported model: {model_name}"
        )