from fastapi import FastAPI
from .routes import users_router

version = 'v1'

app = FastAPI(
    title="User Service",
    description="A REST API for a user web service",
    version=version
)

app.include_router(users_router, prefix=f'/api/{version}/users', tags=['users'])

