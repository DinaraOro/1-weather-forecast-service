FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN pip install uv

RUN uv pip install --system .

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "frontend/app.py", "--server.address=0.0.0.0"]