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
    image_url: str | None = Field(
        sa_column=Column(pg.VARCHAR, nullable=True, default=None)
    )
    category_uid: uuid.UUID | None = Field(
        sa_column=Column(pg.UUID, nullable=True, default=None)
    )
    category_name: str | None = Field(
        sa_column=Column(pg.VARCHAR, nullable=True, default=None)
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))