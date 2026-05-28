from pydantic import BaseModel


class TrainRequest(BaseModel):

    city: str

    model_name: str


class TrainResponse(BaseModel):

    MAE: float

    RMSE: float