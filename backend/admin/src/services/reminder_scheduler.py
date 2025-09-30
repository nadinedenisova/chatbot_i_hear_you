import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from schemas.entity import HistoryCreate
from services.telegram_bot import TelegramBot
from db.db_engine import DBEngine
from utils.pagination import PaginatedParams  # если используешь пагинацию
from core.settings import settings
import logging

logger = logging.getLogger(__name__)


def start_scheduler(
    bot: TelegramBot,
    db_engine: DBEngine,
):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        notify_inactive_users,
        IntervalTrigger(minutes=settings.reminder_polling_interval_in_minutes),  # TODO заменить на час
        # IntervalTrigger(hours=1),
        kwargs={"bot": bot, "db_engine": db_engine},
        name="notify_inactive_users",
    )
    scheduler.start()


async def notify_inactive_users(bot: TelegramBot, db_engine: DBEngine):
    logger.info("🔔 Запущена задача по проверке неактивных пользователей")

    users = await db_engine.get_long_time_lost_users(
        days_count=10, pagination=PaginatedParams(page_size=1000, page_number=1)
    )
    if not users:
        logger.info("No long time lost users")

    root_node = (  # корень нужен, чтобы назначить пользователю, что тот его посмотрел
        await db_engine.get_menu_root()
    )  # не знаю надо ли проверять есть ли корень

    for user in users:
        try:
            await bot.send_message(
                user_id=int(user.id),
                text="Привет! Мы давно не видели твоей активности. Возвращайся! 😊",
            )
            await db_engine.create_history_record(
                user_id=user.id,
                history_data=HistoryCreate(
                    menu_id=root_node.id, action_date=datetime.datetime.now()
                ),
            )  # пользователю добавляется действие для того чтобы через час ему опять не пришло уведомление
        except Exception as e:
            logger.warning(f"Ошибка при отправке сообщения пользователю {user.id}: {e}")
