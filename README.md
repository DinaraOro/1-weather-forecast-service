# Weather Forecast Service

## Описание проекта

Weather Forecast Service — это end-to-end ML-сервис для прогнозирования температуры воздуха.

Пользователь может:

* выбрать город;
* выбрать модель прогнозирования;
* получить прогноз температуры на 7 дней;
* сравнить прогноз с фактическими погодными данными;
* переобучить модель;
* обновить погодные данные через API.

Проект демонстрирует полный ML lifecycle:

* загрузка данных;
* предобработка;
* обучение моделей;
* сохранение артефактов;
* инференс;
* обновление данных;
* визуализация результатов;
* Docker-развертывание.

---

# Архитектура проекта

## Frontend

* Streamlit
* интерактивный интерфейс;
* визуализация прогнозов;
* управление моделями.

## Backend

* FastAPI
* REST API;
* inference endpoints;
* retraining pipeline;
* refresh data pipeline.

## Хранение данных

* CSV-датасеты;
* артефакты моделей;
* метрики моделей.

## ML-модели

Проект поддерживает три подхода к прогнозированию:

| Модель        | Тип                     |
| ------------- | ----------------------- |
| Random Forest | Feature-based ML        |
| ARIMA         | Statistical Time Series |
| LSTM          | Neural Time Series      |

---

# Функциональность

## Загрузка погодных данных

* автоматическая загрузка данных через Open-Meteo API;
* локальное сохранение датасетов;
* обновление данных до актуальной даты.

## Прогнозирование

* прогноз температуры на 7 дней;
* recursive forecasting;
* сравнение forecast vs actual.

## Переобучение моделей

* retrain через UI;
* автоматическое сохранение артефактов;
* пересчет метрик качества.

## Визуализация

Интерактивный график отображает:

* historical temperatures;
* forecast;
* actual future temperatures.

---

# Структура проекта

```text
1-weather-forecast-service/
├── artifacts/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── data/
│   │   ├── models/
│   │   ├── services/
│   │   └── schemas/
├── data/
│   └── raw/
├── frontend/
├── docker-compose.yml
└── README.md
```

---

# API Endpoints

## Получение прогноза

```http
POST /predict
```

Пример запроса:

```json
{
  "city": "Lisbon",
  "model_name": "random_forest",
  "forecast_date": "2026-05-20"
}
```

---

## Переобучение модели

```http
POST /train
```

Пример запроса:

```json
{
  "city": "Lisbon",
  "model_name": "lstm"
}
```

---

## Обновление погодных данных

```http
POST /refresh-data
```

Query params:

```text
city=Lisbon
```

---

## Получение метрик

```http
GET /metrics
```

---

## Получение погодных данных

```http
GET /weather-data
```

---

# ML Pipeline

## Random Forest

Feature-based forecasting с использованием:

* lag features;
* rolling averages;
* calendar features.

## ARIMA

Statistical forecasting:

* autoregression;
* differencing;
* moving average.

Конфигурация:

```text
ARIMA(7,1,1)
```

## LSTM

Neural forecasting на базе PyTorch:

* sequence windows;
* LSTM layers;
* recursive prediction.

---

# Источник данных

## Open-Meteo API

Используются:

* Geocoding API;
* Historical Weather API.

Официальный сайт:

https://open-meteo.com/

---

# Запуск проекта

## 1. Клонирование репозитория

```bash
git clone <repository_url>
cd 1-weather-forecast-service
```

---

## 2. Запуск контейнеров

```bash
docker compose up --build
```

---

# Адреса сервисов

## Frontend

```text
http://localhost:8501
```

## Backend API

```text
http://localhost:8000
```

---

# Пример сценария работы

1. Выбрать город.
2. Выбрать модель.
3. Указать дату прогноза.
4. Получить прогноз.
5. Сравнить forecast vs actual.
6. Обновить погодные данные.
7. Переобучить модель.

---

# Используемые технологии

## Backend

* FastAPI
* Pandas
* Scikit-learn
* Statsmodels
* PyTorch

## Frontend

* Streamlit
* Plotly

## Infrastructure

* Docker
* Docker Compose

---

# Возможные улучшения

* hyperparameter tuning;
* experiment tracking;
* Airflow orchestration;
* cloud deployment;
* GPU training;
* confidence intervals;
* model monitoring;
* MLflow integration.

---

# Definition of Done

Проект удовлетворяет следующим требованиям:

* Dockerized deployment;
* web-интерфейс прогнозирования;
* поддержка нескольких типов моделей;
* forecast vs actual visualization;
* автоматическое обновление данных;
* retraining pipeline;
* сохранение артефактов моделей;
* модульная backend-архитектура;
* визуализация метрик качества.
