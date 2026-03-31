from fastapi import FastAPI
from .routes import inventory_router
from contextlib import asynccontextmanager
from .rabbit_consumer import ProductCreatedConsumer
from .config import Config
import uvicorn

consumer = ProductCreatedConsumer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await consumer.connect()
    await consumer.consume()
    app.state.rabbit_consumer = consumer
    try:
        yield
    finally:
        await consumer.close()

version = "v1"

app = FastAPI(
    title="Inventory Service",
    description="A REST API for an inventory web service",
    version=version,
    lifespan=lifespan
)

app.include_router(inventory_router, prefix=f"/api/{version}/inventory", tags=["inventory"])

port = Config.PORT

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)