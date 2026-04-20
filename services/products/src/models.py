from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from decimal import Decimal
from datetime import datetime

class Product(SQLModel, table=True):
    __tablename__ = "products"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    name: str
    description: str
    price: Decimal = Field(
        sa_column=Column(pg.NUMERIC(10, 2), nullable=False)
    )
    image_url: str | None = Field(
        sa_column=Column(pg.VARCHAR, nullable=True, default=None)
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))