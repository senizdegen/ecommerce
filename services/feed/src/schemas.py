from pydantic import BaseModel
from decimal import Decimal
import uuid
from typing import Optional


class ProductCreateModel(BaseModel):
    product_uid: uuid.UUID
    name: str
    description: str
    price: Decimal
    available_quantity: int
    image_url: Optional[str] = None
    category_uid: Optional[uuid.UUID] = None
    category_name: Optional[str] = None


class ProductUpdateModel(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    image_url: str | None = None
    category_uid: uuid.UUID | None = None
    category_name: str | None = None


class FeedProductModel(BaseModel):
    uid: uuid.UUID
    name: str
    description: str
    price: Decimal
    available_quantity: int
    image_url: Optional[str] = None
    category_uid: Optional[uuid.UUID] = None
    category_name: Optional[str] = None

    class Config:
        from_attributes = True

class CategoryModel(BaseModel):
    uid: Optional[uuid.UUID] = None
    name: str

    class Config:
        from_attributes = True