from pathlib import Path

import joblib
import numpy as np
import torch
import torch.nn as nn


BASE_DIR = Path(__file__).resolve().parent.parent

RF_MODEL_PATH = BASE_DIR / "artifacts" / "random_forest.pkl"
ARIMA_MODEL_PATH = BASE_DIR / "artifacts" / "arima.pkl"
LSTM_MODEL_PATH = BASE_DIR / "artifacts" / "lstm_model.pth"
LSTM_SCALER_PATH = BASE_DIR / "artifacts" / "lstm_scaler.pkl"


class LSTMModel(nn.Module):

    def __init__(self):

        super().__init__()

        self.lstm = nn.LSTM(
            input_size=1,
            hidden_size=32,
            batch_first=True,
        )

        self.fc = nn.Linear(
            32,
            1,
        )

    def forward(self, x):

        output, (hidden, cell) = self.lstm(x)

        hidden = hidden[-1]

        prediction = self.fc(hidden)

        return prediction


rf_model = joblib.load(RF_MODEL_PATH)

arima_model = joblib.load(ARIMA_MODEL_PATH)

lstm_scaler = joblib.load(LSTM_SCALER_PATH)

lstm_model = LSTMModel()
lstm_model.load_state_dict(
    torch.load(
        LSTM_MODEL_PATH,
        map_location=torch.device("cpu"),
    )
)
lstm_model.eval()


def predict_temperature(request):

    if request.model == "RandomForest":

        return predict_random_forest(request)

    elif request.model == "ARIMA":

        return predict_arima()

    elif request.model == "LSTM":

        return predict_lstm(request)

    else:

        raise ValueError(
            f"Unknown model: {request.model}"
        )


def predict_random_forest(request):

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

    prediction = rf_model.predict(features)

    return float(prediction[0])


def predict_arima():

    prediction = arima_model.forecast(
        steps=1
    )

    return float(prediction[0])


def predict_lstm(request):

    sequence = np.array([
        request.lag_7,
        request.lag_2,
        request.lag_1,
    ]).reshape(-1, 1)

    scaled_sequence = lstm_scaler.transform(
        sequence
    )

    input_tensor = torch.tensor(
        scaled_sequence,
        dtype=torch.float32,
    ).unsqueeze(0)

    with torch.no_grad():

        scaled_prediction = lstm_model(
            input_tensor
        )

    prediction = lstm_scaler.inverse_transform(
        scaled_prediction.numpy()
    )

    return float(prediction[0][0])