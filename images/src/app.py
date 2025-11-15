from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/", response_class=PlainTextResponse)
def root():
    return "Hello from IMAGES service!"

@app.get("/healthz", response_class=PlainTextResponse)
def healthz():
    return "ok"
