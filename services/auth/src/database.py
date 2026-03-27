from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import create_engine, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from .config import Config
from sqlalchemy.orm import sessionmaker

async_engine = AsyncEngine(
    create_engine(
        url = Config.DATABASE_URL,
        echo=True
    )
)

async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        yield session
