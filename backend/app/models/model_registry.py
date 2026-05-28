from app.models.random_forest_model import (
    RandomForestWeatherModel,
)

from app.models.arima_model import (
    ARIMAModel,
)

from app.models.lstm_model import (
    LSTMWeatherModel,
)


MODELS = {
    "random_forest": RandomForestWeatherModel,
    "arima": ARIMAModel,
    "lstm": LSTMWeatherModel,
}