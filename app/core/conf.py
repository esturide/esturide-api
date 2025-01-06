from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class DefaultSettings(BaseSettings):
    api_host: str
    api_port: int

    db_name: str
    db_username: str
    db_password: str
    db_port: int
    db_host: str
    db_url: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = ConfigDict(
        env_file=".env"
    )

c
settings = DefaultSettings()
