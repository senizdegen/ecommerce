from fastapi import FastAPI
from .routes import cart_router
from fastapi.middleware.cors import CORSMiddleware

version = "v1"

app = FastAPI(
    title="Cart Service",
    description="A REST API for a cart web service",
    version=version,
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ecommerce-client-admb.vercel.app",
        "https://ecommerce-admin-admb.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cart_router, prefix=f"/api/{version}/cart", tags=["cart"])