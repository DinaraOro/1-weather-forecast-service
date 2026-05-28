import numpy as np

import pandas as pd


def create_lstm_sequences(
    df: pd.DataFrame,
    sequence_length: int = 7,
):

    temperatures = df["temperature"].values

    X = []

    y = []

    for i in range(
        sequence_length,
        len(temperatures),
    ):

        sequence = temperatures[
            i - sequence_length:i
        ]

        target = temperatures[i]

        X.append(sequence)

        y.append(target)

    X = np.array(X)

    y = np.array(y)

    return X, y