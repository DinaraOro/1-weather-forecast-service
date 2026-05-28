import joblib
import numpy as np

from pathlib import Path

from sklearn.metrics import (
    mean_absolute_error,
    root_mean_squared_error,
)

from statsmodels.tsa.arima.model import (
    ARIMA,
)


BASE_DIR = Path(__file__).resolve().parents[3]

ARTIFACTS_DIR = BASE_DIR / "artifacts"


class ARIMAModel:

    def __init__(self):

        self.model = None

        self.fitted_model = None

    def train(self, df):

        series = df["temperature"]

        train_size = int(len(series) * 0.8)

        train = series[:train_size]

        test = series[train_size:]

        self.model = ARIMA(
            train,
            order=(7, 1, 1),
        )

        self.fitted_model = (
            self.model.fit()
        )

        predictions = (
            self.fitted_model.forecast(
                steps=len(test)
            )
        )

        mae = mean_absolute_error(
            test,
            predictions,
        )

        rmse = root_mean_squared_error(
            test,
            predictions,
        )

        return {
            "MAE": float(mae),
            "RMSE": float(rmse),
        }

    def predict(
        self,
        steps=7,
    ):

        predictions = (
            self.fitted_model.forecast(
                steps=steps
            )
        )

        return predictions.tolist()

    def save(self):

        ARTIFACTS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        filepath = (
            ARTIFACTS_DIR
            / "arima.pkl"
        )

        joblib.dump(
            self.fitted_model,
            filepath,
        )

    def load(self):

        filepath = (
            ARTIFACTS_DIR
            / "arima.pkl"
        )

        self.fitted_model = (
            joblib.load(filepath)
        )