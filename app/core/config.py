from pydantic import PostgresDsn
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Настройки приложение
    APP__TITLE: str = "Сервис для бронирования столиков"
    APP__DESCRIPTION: str = """
    Сервис позволяет создавать, просматривать и удалять брони,
    а также управлять столиками и временными слотами.
    """

    # Настройки системные
    SYSTEM__DEBUG: bool = False

    # Настройки базы данных
    DB__POSTGRES_DSN: PostgresDsn = Field(default=...)


settings = Settings()
