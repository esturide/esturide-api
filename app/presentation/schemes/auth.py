from pydantic import BaseModel, Field, SecretStr

from app.core.types import Token, UserCode


class AccessLogin(BaseModel):
    username: UserCode
    password: SecretStr


class AccessCredential(BaseModel):
    token: Token | str = Field(..., title="Access token", alias='token')
    type: str = Field("bearer", title="Token type", alias='type')


class AccessCredentialForm(BaseModel):
    access_token: Token | str = Field(..., title="Access token")
    token_type: str = Field("bearer", title="Token type")
