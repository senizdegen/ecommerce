from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from typing import Optional


class UserProfileModel(BaseModel):
    uid: uuid.UUID
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime


class UserProfileCreateModel(BaseModel):
    uid: uuid.UUID
    first_name: str
    last_name: str
    email: str
    is_admin: bool = False


class UserProfileUpdateModel(BaseModel):  # добавить
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    is_admin: Optional[bool] = None  # только админ может менять это поле