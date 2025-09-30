from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""

    project_name: str = "API системы администрирования бота"

    # postgres
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str

    # redis
    redis_port: int
    redis_host: str
    redis_db: int

    # bot
    bot_token: str
    reminder_polling_interval_in_minutes: int


settings = Settings()  # type: ignore
