from pydantic import BaseModel
from decimal import Decimal
import uuid


class ProductCreateModel(BaseModel):
    product_uid: uuid.UUID
    name: str
    description: str
    price: Decimal
    available_quantity: Decimal


class ProductUpdateModel(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None