import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st


st.title("Weather Forecast Service")


city = st.selectbox(
    "Select city",
    [
        "Lisbon",
        "Amsterdam",
        "Paris",
        "Berlin",
    ],
)


model_name = st.selectbox(
    "Select model",
    [
        "random_forest",
        "arima",
        "lstm",
    ],
)


forecast_date = st.date_input(
    "Forecast date"
)


if st.button("Predict"):

    payload = {
        "city": city,
        "model_name": model_name,
        "forecast_date": str(forecast_date),
    }

    try:

        # Forecast request
        predict_response = requests.post(
            "http://backend:8000/predict",
            json=payload,
            timeout=30,
        )

        forecast = (
            predict_response.json()[
                "forecast"
            ]
        )

        forecast_df = pd.DataFrame(
            forecast
        )

        # Historical weather data
        history_response = requests.get(
            "http://backend:8000/weather-data",
            params={
                "city": city,
            },
            timeout=30,
        )

        history_data = (
            history_response.json()
        )

        history_df = pd.DataFrame(
            history_data
        )

        # Convert dates
        history_df["date"] = pd.to_datetime(
            history_df["date"]
        )

        forecast_df["date"] = pd.to_datetime(
            forecast_df["date"]
        )

        forecast_start = pd.to_datetime(
            forecast_date
        )

        # Split historical and actual future
        past_history_df = history_df[
            history_df["date"] < forecast_start
        ]

        # only last 30 days
        past_history_df = (
            past_history_df
            .sort_values("date")
            .tail(30)
        )
        actual_future_df = history_df[
            history_df["date"] >= forecast_start
        ]

        # Forecast table
        st.subheader(
            "7-Day Forecast"
        )

        st.dataframe(
            forecast_df
        )

        # Create graph
        fig = go.Figure()

        # Historical data
        fig.add_trace(
            go.Scatter(
                x=past_history_df["date"],
                y=past_history_df["temperature"],
                mode="lines",
                name="Historical Temperature",
            )
        )

        # Forecast
        fig.add_trace(
            go.Scatter(
                x=forecast_df["date"],
                y=forecast_df["prediction"],
                mode="lines+markers",
                name="Forecast",
            )
        )

        # Actual future data
        fig.add_trace(
            go.Scatter(
                x=actual_future_df["date"],
                y=actual_future_df["temperature"],
                mode="lines+markers",
                name="Actual Temperature",
            )
        )

        fig.update_layout(
            title="Weather Forecast",
            xaxis_title="Date",
            yaxis_title="Temperature",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        # Metrics
        metrics_response = requests.get(
            "http://backend:8000/metrics",
            params={
                "model_name": model_name
            },
            timeout=30,
        )

        metrics = metrics_response.json()

        st.subheader(
            "Model Metrics"
        )

        st.write(metrics)

    except Exception as e:

        st.error(str(e))


if st.button("Retrain model"):

    payload = {
        "city": city,
        "model_name": model_name,
    }

    try:

        response = requests.post(
            "http://backend:8000/train",
            json=payload,
            timeout=300,
        )

        metrics = response.json()

        st.success(
            "Model retrained successfully"
        )

        st.write(metrics)

    except Exception as e:

        st.error(str(e))

if st.button("Refresh weather data"):

    try:

        response = requests.post(
            "http://backend:8000/refresh-data",
            params={
                "city": city,
            },
            timeout=300,
        )

        result = response.json()

        st.success(
            "Weather data refreshed"
        )

        st.write(result)

    except Exception as e:

        st.error(str(e))