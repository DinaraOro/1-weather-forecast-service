from fastapi import FastAPI

from app.api.routes.predict import (
    router as predict_router,
)

from app.api.routes.train import (
    router as train_router,
)

from app.api.routes.metrics import (
    router as metrics_router,
)


from app.api.routes.weather_data import (
    router as weather_data_router,
)

from app.api.routes.refresh_data import (
    router as refresh_data_router,
)

app = FastAPI(
    title="Weather Forecast Service",
)


app.include_router(predict_router)

app.include_router(train_router)

app.include_router(metrics_router)

app.include_router(weather_data_router)

app.include_router(
    refresh_data_router
)