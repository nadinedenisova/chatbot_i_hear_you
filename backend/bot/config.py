from environs import Env

# Создаем екземпляр класса Env и
# добавляем в переменные окружения данные из .env
env = Env()
env.read_env()

# Основные настройки
BOT_TOKEN = env.str("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не установлен в .env файле!")
DEBUG = env.bool("DEBUG", default=False)
