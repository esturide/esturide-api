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

    secret_key: str = "your-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = ConfigDict(
        env_file=".env"
    )


settings = DefaultSettings()

@lru_cache
def get_settings():
    return DefaultSettings()
