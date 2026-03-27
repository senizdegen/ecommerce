from fastapi import FastAPI
from .routes import auth_router

version = 'v1'

app = FastAPI(
    title="Auth Service",
    description="A REST API for a auth web service",
    version=version
)

app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
