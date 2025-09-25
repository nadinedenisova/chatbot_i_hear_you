from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""

    project_name: str = 'API системы администрирования бота'


settings = Settings()
