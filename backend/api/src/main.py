from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.routers.v1 import example
from .settings import settings


app = FastAPI(
    title=settings.project_name,
    description='Предоставляет эндпоинты для управления ботом.',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


app.include_router(example.router, prefix='/api/v1/example', tags=['Пример'])
