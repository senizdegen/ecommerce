from fastapi import FastAPI
from .routes import feed_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .rabbit_consumer import ProductConsumer

consumer = ProductConsumer()

version = "v1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    await consumer.connect()
    await consumer.consume()
    app.state.rabbit_consumer = consumer
    try:
        yield
    finally:
        await consumer.close()

app = FastAPI(
    title="FEED SERVICE", 
    description="Rest api for Feed web service", 
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

app.include_router(feed_router, prefix="/api/{version}/feed", tags=["feed"])


