from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from decimal import Decimal
from datetime import datetime

class FeedProduct(SQLModel, table=True):
    __tablename__ = "feed_products"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True)
    )
    name: str
    description: str
    price: Decimal = Field(
        sa_column=Column(pg.NUMERIC(10, 2), nullable=False)
    )
    available_quantity: int
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
