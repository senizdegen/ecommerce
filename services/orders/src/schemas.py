from pydantic import BaseModel
import uuid
from decimal import Decimal
from datetime import datetime
from typing import List


class OrderItemModel(BaseModel):
    uid: uuid.UUID
    order_uid: uuid.UUID
    product_uid: uuid.UUID
    quantity: int
    price_snapshot: Decimal
    created_at: datetime

class OrderModel(BaseModel):
    uid: uuid.UUID
    user_uid: uuid.UUID
    total_amount: Decimal
    status: str
    created_at: datetime
    updated_at: datetime

class OrderWithItemsResponse(BaseModel):
    order: OrderModel
    items: List[OrderItemModel]

class StatusUpdateRequest(BaseModel):
    status: str