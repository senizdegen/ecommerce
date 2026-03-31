from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routes import users_router
from .rabbit_consumer import UserCreatedConsumer
from .config import Config
import uvicorn

consumer = UserCreatedConsumer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await consumer.connect()
    await consumer.consume()
    app.state.rabbit_consumer = consumer
    try:
        yield
    finally:
        await consumer.close()

version = 'v1'

app = FastAPI(
    title="User Service",
    description="A REST API for a user web service",
    version=version,
    lifespan=lifespan
)

app.include_router(users_router, prefix=f'/api/{version}/users', tags=['users'])

port = Config.PORT

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

