from pydantic import BaseModel, Field

from app.core.types import Token


class CredentialsAuthenticationWebsocket(BaseModel):
    access_token: Token | str = Field(..., title="Access token", alias='accessToken')
