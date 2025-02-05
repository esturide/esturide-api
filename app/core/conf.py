from functools import lru_cache

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class DefaultSettings(BaseSettings):
    api_host: str = "127.0.0.1"
    api_port: int = "8000"

    db_name: str = ""
    db_username: str = ""
    db_password: str = ""
    db_port: int = ""
    db_host: str = ""
    db_url: str = ""

    cache_password: str
    cache_port: int
    cache_host: str
    cache_databases: int

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = ConfigDict(
        env_file=".env"
    )


settings = DefaultSettings()

@lru_cache
def get_settings():
    return DefaultSettings()

