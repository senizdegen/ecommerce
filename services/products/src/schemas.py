from pydantic import BaseModel
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional


class ProductModel(BaseModel):
    uid: uuid.UUID
    name: str
    description: str
    price: Decimal
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class ProductCreateModel(BaseModel):
    name: str
    description: str
    price: Decimal
    available_quantity: int  # было Decimal — исправил, количество это int

class ProductUpdateModel(BaseModel):
    name: str
    description: str
    price: Decimal