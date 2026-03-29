from fastapi import FastAPI
from .routes import auth_router
from .config import Config
from .rabbit import RabbitMQClient
from contextlib import asynccontextmanager

version = "v1"
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
    title="Auth Service",
    description="A REST API for a auth web service",
    version=version,
    lifespan=lifespan,
)

app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
