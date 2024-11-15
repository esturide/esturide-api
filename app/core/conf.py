from pydantic_settings import BaseSettings


class DefaultSettings(BaseSettings):
    db_name: str
    db_username: str
    db_password: str
    db_port: int
    db_host: str
    db_url: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = DefaultSettings()
