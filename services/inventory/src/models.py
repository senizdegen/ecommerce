from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import CheckConstraint
import uuid
from datetime import datetime


class Inventory(SQLModel, table=True):
    __tablename__ = "inventory"

    product_uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, nullable=False)
    )

    available_quantity: int = Field(
        sa_column=Column(pg.INTEGER, nullable=False, default=0)
    )

    reserved_quantity: int = Field(
        sa_column=Column(pg.INTEGER, nullable=False, default=0)
    )

    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))


    __table_args__ = (
        CheckConstraint("available_quantity >= 0", name="check_available_non_negative"),
        CheckConstraint("reserved_quantity >= 0", name="check_reserved_non_negative"),
    )
