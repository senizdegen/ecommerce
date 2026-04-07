from fastapi import FastAPI
from .routes import cart_router
from .config import Config
from fastapi.middleware.cors import CORSMiddleware

version = "v1"

app = FastAPI(
    title="Cart Service",
    description="A REST API for a cart web service",
    version=version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cart_router, prefix=f"/api/{version}/cart", tags=["cart"])