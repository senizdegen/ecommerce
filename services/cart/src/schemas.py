from pydantic import BaseModel
import uuid
from datetime import datetime


class CartItemModel(BaseModel):
    uid: uuid.UUID
    cart_uid: uuid.UUID
    product_uid: uuid.UUID
    quantity: int
    created_at: datetime
    updated_at: datetime


class CartModel(BaseModel):
    uid: uuid.UUID
    user_uid: uuid.UUID
    created_at: datetime
    updated_at: datetime


class CartWithItemsResponse(BaseModel):
    cart: CartModel
    items: list[CartItemModel]


class AddToCartRequest(BaseModel):
    product_uid: uuid.UUID
    quantity: int


class UpdateCartItemRequest(BaseModel):
    quantity: int