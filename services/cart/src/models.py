from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime


class Cart(SQLModel, table=True):
    __tablename__ = "carts"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    )
    user_uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, unique=True, index=True)
    )
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now)
    )


class CartItem(SQLModel, table=True):
    __tablename__ = "cart_items"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    )
    cart_uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, index=True)
    )
    product_uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, index=True)
    )
    quantity: int = Field(
        sa_column=Column(pg.INTEGER, nullable=False)
    )
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now)
    )