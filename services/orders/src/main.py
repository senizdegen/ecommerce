from fastapi import FastAPI
from .routes import order_router
from .config import Config
from contextlib import asynccontextmanager
import uvicorn

version = "v1"

app = FastAPI(
    title="Order Service",
    description="A REST API for a order web service",
    version=version,
)

app.include_router(order_router, prefix=f"/api/{version}/orders", tags=["orders"])