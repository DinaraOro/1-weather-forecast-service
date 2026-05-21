from pathlib import Path

import joblib
import numpy as np


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR / "artifacts" / "random_forest.pkl"
)


def predict_temperature(request):

    model = joblib.load(MODEL_PATH)

    features = np.array([
        [
            request.lag_1,
            request.lag_2,
            request.lag_7,
            request.rolling_mean_7,
            request.precipitation,
            request.wind,
        ]
    ])

    prediction = model.predict(features)

    return float(prediction[0])