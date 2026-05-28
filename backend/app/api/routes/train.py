from fastapi import APIRouter

from app.schemas.train_schema import (
    TrainRequest,
    TrainResponse,
)

from app.services.training_service import (
    train_model,
)


router = APIRouter()


@router.post(
    "/train",
    response_model=TrainResponse,
)
def train(
    request: TrainRequest,
):

    metrics = train_model(
        model_name=request.model_name,
        city=request.city,
    )

    return TrainResponse(
        MAE=metrics["MAE"],
        RMSE=metrics["RMSE"],
    )