from pydantic import BaseModel
import uuid
from datetime import datetime
from decimal import Decimal


class ProductModel(BaseModel):
    uid: uuid.UUID
    name: str
    description: str
    price: Decimal
    created_at: datetime
    updated_at: datetime

class ProductCreateModel(BaseModel):
    name: str
    description: str
    price: Decimal
    available_quantity: Decimal

class ProductUpdateModel(BaseModel):
    name: str
    description: str
    price: Decimal