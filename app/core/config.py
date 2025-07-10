from pydantic import PostgresDsn
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DSN: PostgresDsn = Field(default=...)


settings = Settings()
