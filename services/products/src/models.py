from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import ForeignKey  # добавить
import uuid
from decimal import Decimal
from datetime import datetime
from typing import Optional


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, unique=True))
    description: str | None = Field(sa_column=Column(pg.VARCHAR, nullable=True, default=None))

    products: list["Product"] = Relationship(back_populates="category")


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
    category_uid: uuid.UUID | None = Field(
        sa_column=Column(pg.UUID, ForeignKey("categories.uid"), nullable=True)  # исправлено
    )
    category: Optional[Category] = Relationship(back_populates="products")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))