from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.api.v1 import example
from src.db.redis import _redis
from src.core.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if _redis:
        await _redis.aclose()


app = FastAPI(
    title=settings.project_name,
    description='Предоставляет эндпоинты для управления ботом.',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


app.include_router(example.router, prefix='/api/v1/example', tags=['Пример'])
