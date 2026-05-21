# Weather Forecast Service

## Описание проекта

Weather Forecast Service — это ML-сервис для прогнозирования средней температуры воздуха на основе исторических погодных данных.

Проект реализует полный pipeline production-style ML системы:

- обучение модели машинного обучения
- feature engineering для временных рядов
- backend API на FastAPI
- frontend интерфейс на Streamlit
- inference через HTTP API
- взаимодействие frontend ↔ backend ↔ model

---

# Цель проекта

Основная цель проекта — построить end-to-end ML сервис для прогнозирования температуры и продемонстрировать навыки:

- Machine Learning
- Time Series Forecasting
- Feature Engineering
- Backend Development
- API Development
- ML Model Serving
- Frontend Integration
- Debugging и networking

---

# Используемый стек

## Machine Learning

- pandas
- numpy
- scikit-learn
- statsmodels
- PyTorch

## Backend

- FastAPI
- Uvicorn
- Pydantic

## Frontend

- Streamlit

## Visualization

- Plotly

---

# Датасет

Используются погодные данные по Амстердаму за 2023–2024 годы.

Основные признаки:

- temperature_2m_mean
- temperature_2m_max
- temperature_2m_min
- precipitation_sum
- wind_speed_10m_max

---

# Feature Engineering

Для прогнозирования использовались лаговые признаки и rolling statistics.

## Используемые признаки

| Feature | Описание |
|---|---|
| lag_1 | температура за 1 день до прогноза |
| lag_2 | температура за 2 дня до прогноза |
| lag_7 | температура за 7 дней до прогноза |
| rolling_mean_7 | средняя температура за последние 7 дней |
| precipitation_sum | количество осадков |
| wind_speed_10m_max | максимальная скорость ветра |

---

# Используемые модели

В проекте были протестированы несколько подходов.

## Random Forest Regressor

Основная production-модель проекта.

Преимущества:

- хорошо работает на tabular data
- устойчив к noise
- не требует нормализации признаков
- хорошо работает на небольших датасетах

---

## ARIMA

Классическая статистическая модель временных рядов.

Недостатки:

- плохо справилась со сложной нелинейной динамикой
- предсказания стремились к усреднению ряда

---

## SARIMA

Seasonal extension модели ARIMA.

Недостатки:

- высокая ошибка
- слабое качество на данном датасете

---

## LSTM

Нейронная сеть для временных рядов.

Особенности:

- использовалась библиотека PyTorch
- применялась нормализация данных через MinMaxScaler
- показала результаты лучше ARIMA, но хуже RandomForest

---

# Сравнение моделей

| Model | MAE | RMSE |
|---|---|---|
| RandomForest | 1.62 | 2.11 |
| ARIMA | 7.58 | 8.99 |
| SARIMA | 10.95 | 12.85 |
| LSTM | 4.23 | 4.98 |

---

# Архитектура проекта

```text
User
↓
Streamlit Frontend
↓
HTTP Request
↓
FastAPI Backend
↓
RandomForest Model
↓
Prediction
↓
JSON Response
↓
Frontend UI
```

---

# Структура проекта

```text
1-weather-forecast-service/
│
├── backend/
│   └── app/
│       ├── main.py
│       ├── schemas/
│       ├── services/
│       └── artifacts/
│
├── frontend/
│   └── app.py
│
├── notebooks/
│
├── data/
│
├── README.md
│
├── pyproject.toml
│
└── uv.lock
```

---

# API Endpoints

## Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

## Prediction Endpoint

```http
POST /predict
```

Request example:

```json
{
  "lag_1": 10.0,
  "lag_2": 9.5,
  "lag_7": 8.0,
  "rolling_mean_7": 9.2,
  "precipitation": 2.1,
  "wind": 20.0
}
```

Response example:

```json
{
  "prediction": 8.72
}
```

---

# Как запустить проект

## 1. Клонировать репозиторий

```bash
git clone <repository_url>
```

---

## 2. Перейти в папку проекта

```bash
cd 1-weather-forecast-service
```

---

## 3. Активировать environment

```bash
source .venv/bin/activate
```

---

## 4. Запустить backend

```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

---

## 5. Запустить frontend

В новом terminal:

```bash
source .venv/bin/activate
streamlit run frontend/app.py
```

---

# Networking issue и debugging

Во время разработки возникла проблема:

- requests из Streamlit возвращали 502 Bad Gateway
- curl при этом работал корректно

Причина оказалась связана с proxy/VPN environment variables.

Проблема была решена через:

```python
session.trust_env = False
```

Это отключило использование системных proxy settings внутри requests.Session().

---

# Возможные улучшения

- Dockerization
- CI/CD pipeline
- deployment в cloud
- подключение real weather API
- model registry
- автоматический retraining
- monitoring и logging
- поддержка нескольких моделей
- async inference

---

# Результат

В рамках проекта был построен полноценный ML web service с production-style архитектурой:

- frontend
- backend
- REST API
- model serving
- inference pipeline
- ML model integration