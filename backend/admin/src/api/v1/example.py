from typing import Annotated

# from redis.asyncio import Redis
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import get_async_session
from db.redis import get_redis


router = APIRouter()


@router.get("/", summary="Базовый пример роутера", include_in_schema=False)
async def base(
    # redis: Annotated[Redis, Depends(get_redis)],
    pg_session: Annotated[AsyncSession, Depends(get_async_session)],
):
    return {"Hello": "World"}
