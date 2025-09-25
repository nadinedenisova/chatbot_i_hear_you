from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.postgres import get_async_session


router = APIRouter()


@router.get(
    '/',
    summary='Базовый пример роутера'
)
async def base(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return {"Hello": "World"}
