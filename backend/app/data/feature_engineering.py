import pandas as pd


def create_features(df: pd.DataFrame):

    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values("date")

    # Lag features

    df["lag_1"] = df["temperature"].shift(1)

    df["lag_2"] = df["temperature"].shift(2)

    df["lag_7"] = df["temperature"].shift(7)

    # Rolling features

    df["rolling_mean_3"] = (
        df["temperature"]
        .rolling(window=3)
        .mean()
    )

    df["rolling_mean_7"] = (
        df["temperature"]
        .rolling(window=7)
        .mean()
    )

    # Calendar features

    df["month"] = df["date"].dt.month

    df["weekday"] = df["date"].dt.weekday

    df["day_of_year"] = df["date"].dt.dayofyear

    # Remove NaN after lagging

    df = df.dropna()

    return df