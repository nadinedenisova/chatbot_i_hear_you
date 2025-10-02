from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles

from src.api.v1 import example, menu_router, users_router, file_router
from src.core.settings import settings
from src.db.db_engine import create_db_engine
from src.db.postgres import async_session_maker
from src.services.reminder_scheduler import start_scheduler
from src.services.telegram_bot import get_telegram_bot


@asynccontextmanager
async def lifespan(app: FastAPI):
    telegram_bot = get_telegram_bot()

    async with async_session_maker() as session:
        db_engine = create_db_engine(session)

        start_scheduler(bot=telegram_bot, db_engine=db_engine)

        yield

        await telegram_bot.bot.session.close()


app = FastAPI(
    title=settings.project_name,
    description="Предоставляет эндпоинты для управления ботом.",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


app.include_router(example.router, prefix="/api/v1/example", tags=["Пример"])
app.include_router(menu_router.router, prefix="/api/v1/menu", tags=["Меню"])
app.include_router(users_router.router,
                   prefix="/api/v1/users", tags=["Пользователи"])

app.include_router(file_router.router, prefix="/api/files",
                   tags=["Загрузка файлов"])

app.mount("/uploaded_content", StaticFiles(directory="uploaded_content"), name="uploaded_content")
