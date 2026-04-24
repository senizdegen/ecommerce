from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import Optional


class AuthUserModel(BaseModel):
    uid: uuid.UUID
    email: str
    password_hash: str = Field(exclude=True)
    is_verified: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class UserUpdateModel(BaseModel):  # добавить
    email: Optional[str] = Field(default=None, max_length=40)
    password: Optional[str] = Field(default=None, min_length=6)