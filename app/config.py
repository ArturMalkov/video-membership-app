import pathlib
from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    keyspace: str = Field(..., env="ASTRADB_KEYSPACE")
    db_client_id: str = Field(..., env="ASTRADB_CLIENT_ID")
    db_client_secret: str = Field(..., env="ASTRADB_CLIENT_SECRET")

    class Config:
        env_file = pathlib.Path(__file__).parent.parent / ".env"


@lru_cache  # to create a single instance of Settings and use it throughout the whole app
def get_settings() -> Settings:
    return Settings()