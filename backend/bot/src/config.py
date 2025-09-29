from dataclasses import dataclass

from environs import Env


# Создаем екземпляр класса Env и
# добавляем в переменные окружения данные из .env
env = Env()
env.read_env()


@dataclass
class Config:
    """Класс для хранения конфигурационных переменных."""

    BOT_TOKEN = env.str('BOT_TOKEN')
    API_URL = env.str('API_URL')
    API_TIMEOUT: int = 15  # Время ожидания ответа от API в секундах
    LOG_LEVEL = env.str('LOG_LEVEL', default='INFO')


config = Config()
