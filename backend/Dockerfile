FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN pip install uv

RUN uv pip install --system .

COPY . .

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]