from fastapi import FastAPI
from .routes import product_router
from .config import Config
from .rabbit import RabbitMQClient
from contextlib import asynccontextmanager

version = 'v1'
rabbit_client = RabbitMQClient(Config.RABBIT_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit_client.connect()
    app.state.rabbit = rabbit_client
    try:
        yield
    finally:
        await rabbit_client.close()


app = FastAPI(
    title="Product Service",
    description="A REST API for a product web service",
    version=version,
    lifespan=lifespan
)

app.include_router(product_router, prefix=f'/api/{version}/products', tags=['products'])

