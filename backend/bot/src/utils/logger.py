import logging
from pathlib import Path

from config import config


def setup_logging():
    """Настройка логирования для приложения."""

    # Создаем директорию для логов
    Path('logs').mkdir(exist_ok=True)

    # Настройка логирования
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Вывод в консоль
            logging.FileHandler('logs/bot.log', encoding='utf-8'),
        ],
    )

    return logging.getLogger(__name__)
