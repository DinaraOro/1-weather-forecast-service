from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import root_mean_squared_error

from app.data.lstm_preprocessing import (
    create_lstm_sequences,
)

from app.models.base_model import BaseWeatherModel


ARTIFACTS_DIR = Path("/app/artifacts")


class WeatherLSTM(nn.Module):

    def __init__(
        self,
        input_size=1,
        hidden_size=32,
        num_layers=1,
    ):

        super().__init__()

        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
        )

        self.fc = nn.Linear(
            hidden_size,
            1,
        )

    def forward(self, x):

        output, (hidden, cell) = self.lstm(x)

        last_hidden = hidden[-1]

        prediction = self.fc(last_hidden)

        return prediction


class LSTMWeatherModel(BaseWeatherModel):

    def __init__(self):

        self.sequence_length = 7

        self.model = WeatherLSTM()

        self.loss_function = nn.MSELoss()

        self.optimizer = torch.optim.Adam(
            self.model.parameters(),
            lr=0.001,
        )

        self.model_path = (
            ARTIFACTS_DIR / "lstm_model.pth"
        )

    def train(self, df: pd.DataFrame):

        df = df.sort_values("date").copy()

        X, y = create_lstm_sequences(
            df,
            sequence_length=self.sequence_length,
        )

        split_index = int(len(X) * 0.8)

        X_train = X[:split_index]
        y_train = y[:split_index]

        X_test = X[split_index:]
        y_test = y[split_index:]

        X_train_tensor = torch.tensor(
            X_train,
            dtype=torch.float32,
        ).unsqueeze(-1)

        y_train_tensor = torch.tensor(
            y_train,
            dtype=torch.float32,
        ).unsqueeze(-1)

        X_test_tensor = torch.tensor(
            X_test,
            dtype=torch.float32,
        ).unsqueeze(-1)

        epochs = 50

        self.model.train()

        for epoch in range(epochs):

            predictions = self.model(
                X_train_tensor
            )

            loss = self.loss_function(
                predictions,
                y_train_tensor,
            )

            self.optimizer.zero_grad()

            loss.backward()

            self.optimizer.step()

        self.model.eval()

        with torch.no_grad():

            test_predictions = self.model(
                X_test_tensor
            )

        test_predictions = (
            test_predictions
            .squeeze()
            .numpy()
        )

        metrics = {
            "MAE": float(
                mean_absolute_error(
                    y_test,
                    test_predictions,
                )
            ),
            "RMSE": float(
                root_mean_squared_error(
                    y_test,
                    test_predictions,
                )
            ),
        }

        return metrics

    def predict_next(
        self,
        sequence,
    ):

        latest_tensor = torch.tensor(
            sequence,
            dtype=torch.float32,
        ).unsqueeze(0).unsqueeze(-1)

        self.model.eval()

        with torch.no_grad():

            prediction = self.model(
                latest_tensor
            )

        return float(
            prediction.item()
        )
    
    def predict(
        self,
        df: pd.DataFrame,
    ):

        temperatures = (
            df["temperature"]
            .tolist()
        )

        latest_sequence = (
            temperatures[-7:]
        )

        return self.predict_next(
            latest_sequence
        )

    def evaluate(self, df: pd.DataFrame):

        return {}

    def save(self):

        ARTIFACTS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        torch.save(
            self.model.state_dict(),
            self.model_path,
        )

    def load(self):

        self.model.load_state_dict(
            torch.load(
                self.model_path,
                map_location=torch.device("cpu"),
            )
        )

        self.model.eval()