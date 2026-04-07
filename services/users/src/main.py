from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routes import users_router
from .rabbit_consumer import UserCreatedConsumer
from .config import Config
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(users_router, prefix=f'/api/{version}/users', tags=['users'])
