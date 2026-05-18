from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Weather Forecast Service is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
