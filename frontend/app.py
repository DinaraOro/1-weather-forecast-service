import requests
import streamlit as st


st.title("Weather Forecast Service")


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
            "http://127.0.0.1:8000/predict",
            json=payload,
            timeout=5,
        )

        prediction = response.json()["prediction"]

        st.success(
            f"Predicted temperature: {prediction:.2f} °C"
        )

    except Exception as e:

        st.error(str(e))