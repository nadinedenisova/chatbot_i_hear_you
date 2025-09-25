from fastapi import APIRouter


router = APIRouter()


@router.get(
    '/',
    summary='Базовый пример роутера'
)
async def base():
    return {"Hello": "World"}
