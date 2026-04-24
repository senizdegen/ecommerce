from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime


class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profiles"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True)
    )
    first_name: str
    last_name: str
    email: str
    is_verified: bool = Field(default=False)
    is_admin: bool = Field(default=False)  # добавить
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))