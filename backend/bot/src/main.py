import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher

from config import config
from handlers import callback, command
from keyboards import set_main_commands


# Настройка логирования
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Вывод в консоль
        logging.FileHandler("logs/bot.log", encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


async def main() -> None:
    """Основная функция для запуска бота."""
    # Инициализация бота
    bot = Bot(token=config.BOT_TOKEN)

    # Инициализация диспетчера
    dp = Dispatcher()

    # Регистрация роутеров
    dp.include_router(callback.router)
    dp.include_router(command.router)

    await set_main_commands(bot)

    # Удаляем вебхуки и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info('Бот запущен!')

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f'Ошибка при работе бота: {e}')
    finally:
        logger.info('Бот остановлен')
        await bot.session.close()


if __name__ == '__main__':
    logger.info('Запуск приложения')

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Бот остановлен пользователем (Ctrl+C)')
    except Exception as e:
        logger.critical(f'Критическая ошибка: {e}')
