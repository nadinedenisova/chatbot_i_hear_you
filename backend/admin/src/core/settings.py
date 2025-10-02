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

    # bot
    bot_token: str = "yourToken"
    reminder_polling_interval_in_minutes: int


settings = Settings()  # type: ignore
