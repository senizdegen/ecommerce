from pydantic import BaseModel, Field
from uuid import UUID


class InventoryCreate(BaseModel):
    product_uid: UUID
    available_quantity: int = Field(ge=0)


class StockUpdate(BaseModel):
    product_uid: UUID
    quantity: int = Field(gt=0)


class ReserveRequest(BaseModel):
    product_uid: UUID
    quantity: int = Field(gt=0)


class InventoryResponse(BaseModel):
    product_uid: UUID
    available_quantity: int
    reserved_quantity: int

    class Config:
        from_attributes = True