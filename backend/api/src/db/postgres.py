from collections.abc import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.settings import settings


class Base(AsyncAttrs, DeclarativeBase):
    metadata = MetaData(schema="content")


host = settings.postgres_host
port = settings.postgres_port
user = settings.postgres_user
password = settings.postgres_password
dbname = settings.postgres_db
dsn = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}"
async_engine = create_async_engine(dsn)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Возвращает экземпляр сессии SQLAlchemy для работы с Postgres."""

    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
