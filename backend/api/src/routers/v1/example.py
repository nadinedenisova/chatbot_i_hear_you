from typing import Annotated

from redis.asyncio import Redis
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.postgres import get_async_session
from src.db.redis import get_redis


router = APIRouter()


@router.get(
    '/',
    summary='Базовый пример роутера'
)
async def base(
    redis: Annotated[Redis, Depends(get_redis)],
    pg_session: Annotated[AsyncSession, Depends(get_async_session)]
):
    return {"Hello": "World"}
