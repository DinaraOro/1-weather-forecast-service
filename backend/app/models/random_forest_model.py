from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import root_mean_squared_error

from app.models.base_model import BaseWeatherModel


BASE_DIR = Path(__file__).resolve().parents[3]
ARTIFACTS_DIR = BASE_DIR / "artifacts"


FEATURE_COLUMNS = [
    "lag_1",
    "lag_2",
    "lag_7",
    "rolling_mean_3",
    "rolling_mean_7",
    "month",
    "weekday",
    "day_of_year",
]

TARGET_COLUMN = "temperature"


class RandomForestWeatherModel(BaseWeatherModel):

    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
        )

        self.model_path = ARTIFACTS_DIR / "random_forest.pkl"

    def train(self, df: pd.DataFrame):
        df = df.sort_values("date")

        split_index = int(len(df) * 0.8)

        train_df = df.iloc[:split_index]
        test_df = df.iloc[split_index:]

        X_train = train_df[FEATURE_COLUMNS]
        y_train = train_df[TARGET_COLUMN]

        X_test = test_df[FEATURE_COLUMNS]
        y_test = test_df[TARGET_COLUMN]

        self.model.fit(X_train, y_train)

        predictions = self.model.predict(X_test)

        metrics = {
            "MAE": mean_absolute_error(y_test, predictions),
            "RMSE": root_mean_squared_error(y_test, predictions),
        }

        return metrics

    def predict(self, df: pd.DataFrame):
        df = df.sort_values("date")

        latest_row = df.iloc[[-1]]

        X = latest_row[FEATURE_COLUMNS]

        prediction = self.model.predict(X)

        return float(prediction[0])

    def evaluate(self, df: pd.DataFrame):
        df = df.sort_values("date")

        split_index = int(len(df) * 0.8)

        test_df = df.iloc[split_index:]

        X_test = test_df[FEATURE_COLUMNS]
        y_test = test_df[TARGET_COLUMN]

        predictions = self.model.predict(X_test)

        metrics = {
            "MAE": mean_absolute_error(y_test, predictions),
            "RMSE": root_mean_squared_error(y_test, predictions),
        }

        return metrics

    def save(self):
        ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

        joblib.dump(self.model, self.model_path)

    def load(self):
        self.model = joblib.load(self.model_path)