from fastapi import FastAPI
from .routes import cart_router
from .config import Config
import uvicorn

version = "v1"

app = FastAPI(
    title="Cart Service",
    description="A REST API for a cart web service",
    version=version,
)

app.include_router(cart_router, prefix=f"/api/{version}/cart", tags=["cart"])

port = Config.PORT

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)