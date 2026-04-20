from pydantic import BaseModel
from decimal import Decimal
import uuid
from typing import Optional


class ProductCreateModel(BaseModel):
    product_uid: uuid.UUID
    name: str
    description: str
    price: Decimal
    available_quantity: int  # было Decimal — исправил
    image_url: Optional[str] = None


class ProductUpdateModel(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    image_url: str | None = None