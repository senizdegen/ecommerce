from fastapi import FastAPI
from .routes import inventory_router

version = "v1"

app = FastAPI(
    title="Inventory Service",
    description="A REST API for an inventory web service",
    version=version,
)

app.include_router(inventory_router, prefix=f"/api/{version}/inventory", tags=["inventory"])
