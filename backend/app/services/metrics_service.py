import json

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[3]

ARTIFACTS_DIR = BASE_DIR / "artifacts"


def save_metrics(
    model_name: str,
    metrics: dict,
):

    metrics_path = (
        ARTIFACTS_DIR /
        f"{model_name}_metrics.json"
    )

    with open(
        metrics_path,
        "w",
    ) as f:

        json.dump(
            metrics,
            f,
            indent=4,
        )


def load_metrics(
    model_name: str,
):

    metrics_path = (
        ARTIFACTS_DIR /
        f"{model_name}_metrics.json"
    )

    with open(metrics_path) as f:

        metrics = json.load(f)

    return metrics