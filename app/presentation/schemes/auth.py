from pydantic import BaseModel, Field, SecretStr

from app.core.types import Token


class AccessLogin(BaseModel):
    username: str
    password: SecretStr


class AccessCredential(BaseModel):
    access_token: Token | str = Field(..., title="Access token", alias='accessToken')
    token_type: str = Field("bearer", title="Token type", alias='tokenType')
