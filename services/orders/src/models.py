from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime
from decimal import Decimal


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    )

    user_uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, index=True))

    status: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, default="PENDING")
    )

    total_amount: Decimal = Field(
        sa_column=Column(pg.NUMERIC(10, 2), nullable=False, default=0)
    )

    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now)
    )

class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"
    
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    )

    order_uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, index=True)
    )

    product_uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, index=True)
    )

    quantity: int = Field(
        sa_column=Column(pg.INTEGER, nullable=False)
    )

    price_snapshot: Decimal = Field(
        sa_column=Column(pg.NUMERIC(10, 2), nullable=False)
    )

    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now)
    )


