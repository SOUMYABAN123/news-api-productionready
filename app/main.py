from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.logging_config import setup_logging
from app.middleware.request_logging import request_logging_middleware
from app.api.router import api_router

setup_logging()

app = FastAPI(
    title="ML News Classifier API",
    description="Production-ready FastAPI ML service with JWT, Redis caching, rate limiting, monitoring, and UI",
    version="1.0.0",
    docs_url="/documentation",
    redoc_url=None,
)

# Middleware
app.middleware("http")(request_logging_middleware)

# Routes
app.include_router(api_router)

# Prometheus
Instrumentator().instrument(app).expose(app, include_in_schema=False, endpoint="/metrics")

# Static UI
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
