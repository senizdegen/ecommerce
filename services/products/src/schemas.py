from pydantic import BaseModel
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional


class CategoryModel(BaseModel):
    uid: uuid.UUID
    name: str
    description: Optional[str] = None


class ProductModel(BaseModel):
    uid: uuid.UUID
    name: str
    description: str
    price: Decimal
    image_url: Optional[str] = None
    category_uid: Optional[uuid.UUID] = None
    category: Optional[CategoryModel] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductCreateModel(BaseModel):
    name: str
    description: str
    price: Decimal
    available_quantity: int
    category_uid: Optional[uuid.UUID] = None


class ProductUpdateModel(BaseModel):
    name: str
    description: str
    price: Decimal
    category_uid: Optional[uuid.UUID] = None

class CategoryModel(BaseModel):
    uid: uuid.UUID
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True