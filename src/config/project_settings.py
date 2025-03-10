import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

DOTENV_PATH = os.path.join(os.path.dirname(__file__), "..", "..", ".env")


class Settings(BaseSettings):
    pg_url: PostgresDsn = None

    model_config = SettingsConfigDict(
        env_file=DOTENV_PATH, env_file_encoding="utf-8", extra="allow"
    )


settings = Settings()
