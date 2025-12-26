from typing import Literal

from pydantic import PostgresDsn
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Настройки приложение
    APP__TITLE: str = "Сервис для бронирования столиков"
    APP__DESCRIPTION: str = """
    Сервис позволяет создавать, просматривать и удалять брони,

    также управлять столиками и временными слотами.
    """

    # Настройки системные
    APP__DEBUG: bool = False
    RUNTIME__MODE: Literal["prod", "dev"] = "prod"
    UVICORN__APP: str = "main:app"
    UVICORN__HOST: str = "localhost"
    UVICORN__PORT: int = 8000
    UVICORN__RELOAD: Literal["0", "1"] = "0"

    # Настройки базы данных
    DB__POSTGRES_DSN: PostgresDsn = Field(default=...)


settings: Settings = Settings()
