from fastapi import FastAPI
from .routes import order_router
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

version = "v1"

app = FastAPI(
    title="Order Service",
    description="A REST API for a order web service",
    version=version,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ecommerce-pink-alpha-15.vercel.app",
        "https://ecommerce-client-nine-iota.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(order_router, prefix=f"/api/{version}/orders", tags=["orders"])