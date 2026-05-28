from app.data.storage import (
    load_raw_data,
)

from app.data.model_preprocessing import (
    preprocess_for_model,
)

from app.models.model_registry import (
    MODELS,
)

from app.services.metrics_service import (
    save_metrics,
)


def train_model(
    model_name: str,
    city: str,
):

    raw_df = load_raw_data(
        city=city,
    )

    processed_df = preprocess_for_model(
        model_name=model_name,
        raw_df=raw_df,
    )

    model_class = MODELS[
        model_name
    ]

    model = model_class()

    metrics = model.train(
        processed_df
    )

    model.save()

    save_metrics(
        model_name=model_name,
        metrics=metrics,
    )

    return metrics