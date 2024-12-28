from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class DefaultSettings(BaseSettings):
    db_username: str
    db_password: str
    db_uri: str
    db_url: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = ConfigDict(
        env_file=".env"
    )


settings = DefaultSettings()
