from functools import lru_cache
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class DefaultSettings(BaseSettings):
    # API
    api_host: str = "127.0.0.1"
    api_port: int = 8000

    # PostgreSQL
    db_name: str = ""
    db_username: str = ""
    db_password: str = ""
    db_port: int = 0
    db_host: str = ""
    db_url: str = ""

    # Auth
    secret_key: str = "your-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Redis / Cache
    cache_host: str
    cache_port: int
    cache_password: str
    cache_databases: int

    model_config = ConfigDict(
        env_file=".env"
    )

settings = DefaultSettings()

@lru_cache()
def get_settings() -> DefaultSettings:
    return DefaultSettings()
