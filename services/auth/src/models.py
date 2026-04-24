from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime


class AuthUser(SQLModel, table=True):
    __tablename__ = "auth_users"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    email: str = Field(index=True, nullable=False, unique=True)
    password_hash: str = Field(exclude=True)
    is_verified: bool = Field(default=False)
    is_admin: bool = Field(default=False)  # добавить
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))