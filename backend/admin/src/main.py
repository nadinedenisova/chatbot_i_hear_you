from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles

from api.v1 import example, menu_router, users_router,file_router
from db.redis import _redis
from core.settings import settings


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
app.include_router(menu_router.router, prefix='/api/v1/menu', tags=['Меню'])
app.include_router(users_router.router,
                   prefix='/api/v1/users', tags=['Пользователи'])

app.include_router(file_router.router, prefix="/api/files", tags=["Загрузка файлов"])

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
