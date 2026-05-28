from fastapi import APIRouter

from app.services.metrics_service import (
    load_metrics,
)


router = APIRouter()


@router.get("/metrics")
def get_metrics(
    model_name: str,
):

    metrics = load_metrics(model_name)

    return metrics