from app.data.feature_engineering import (
    create_features,
)


def preprocess_for_model(
    model_name: str,
    raw_df,
):

    if model_name == "random_forest":
        return create_features(raw_df)

    if model_name == "arima":
        return raw_df.copy()

    if model_name == "lstm":
        return raw_df.copy()

    raise ValueError(
        f"Unknown model: {model_name}"
    )