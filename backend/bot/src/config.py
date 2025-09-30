from dataclasses import dataclass

from environs import Env


env = Env()
env.read_env()


@dataclass
class Config:
    """Класс для хранения конфигурационных переменных."""

    BOT_TOKEN = env.str('BOT_TOKEN')
    API_URL = env.str('API_URL')
    API_TIMEOUT = env.int('API_TIMEOUT')  # Время ожидания ответа в секундах
    LOG_LEVEL = env.str('LOG_LEVEL', default='INFO')


config = Config()
