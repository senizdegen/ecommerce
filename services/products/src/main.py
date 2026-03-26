from fastapi import FastAPI
from .routes import product_router

version = 'v1'

app = FastAPI(
    title="Product Service",
    description="A REST API for a product web service",
    version=version
)

app.include_router(product_router, prefix=f'/api/{version}/products', tags=['products'])

