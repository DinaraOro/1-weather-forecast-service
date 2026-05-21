import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st


st.title("Weather Forecast Service")


model = st.selectbox(
    "Select model",
    [
        "RandomForest",
        "ARIMA",
        "LSTM",
    ],
)


lag_1 = st.number_input(
    "Temperature yesterday",
    value=10.0,
)

lag_2 = st.number_input(
    "Temperature 2 days ago",
    value=9.5,
)

lag_7 = st.number_input(
    "Temperature 7 days ago",
    value=8.0,
)

rolling_mean_7 = st.number_input(
    "7-day rolling mean",
    value=9.2,
)

precipitation = st.number_input(
    "Precipitation",
    value=2.1,
)

wind = st.number_input(
    "Wind speed",
    value=20.0,
)


if st.button("Predict"):

    payload = {
        "model": model,
        "lag_1": lag_1,
        "lag_2": lag_2,
        "lag_7": lag_7,
        "rolling_mean_7": rolling_mean_7,
        "precipitation": precipitation,
        "wind": wind,
    }

    try:

        session = requests.Session()

        session.trust_env = False

        response = session.post(
            "http://backend:8000/predict",
            json=payload,
            timeout=5,
        )

        prediction = response.json()["prediction"]

        st.success(
            f"Predicted temperature: {prediction:.2f} °C"
        )

        if model == "RandomForest":

            df = pd.read_csv(
                "data/processed/rf_predictions.csv"
            )

        elif model == "LSTM":

            df = pd.read_csv(
                "data/processed/lstm_predictions.csv"
            )
        elif model == "ARIMA":

            df = pd.read_csv(
                "data/processed/arima_predictions.csv"
            )
        else:

            df = pd.read_csv(
                "data/processed/rf_predictions.csv"
            )
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                y=df["actual"],
                mode="lines",
                name="Actual",
            )
        )

        fig.add_trace(
            go.Scatter(
                y=df["predicted"],
                mode="lines",
                name="Predicted",
            )
        )

        fig.update_layout(
            title="Weather Forecast: Actual vs Predicted",
            xaxis_title="Time",
            yaxis_title="Temperature",
            template="plotly_dark",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        mae = (
            abs(
                df["actual"] - df["predicted"]
            )
        ).mean()

        st.write(
            f"Mean Absolute Error (MAE): {mae:.2f} °C"
        )

    except Exception as e:

        st.error(str(e))