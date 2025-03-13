import os
from functools import lru_cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.consts import StorageType

DOTENV_PATH = os.path.join(os.path.dirname(__file__), "..", "..", ".env")


class Settings(BaseSettings):
    pg_url: PostgresDsn = None

    model_config = SettingsConfigDict(
        env_file=DOTENV_PATH, env_file_encoding="utf-8", extra="allow"
    )
    storage_type: StorageType
    s3_url: str
    s3_access_key: str
    s3_secret_key: str
    s3_bucket_name: str


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = Settings()
