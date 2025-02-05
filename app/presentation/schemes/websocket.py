from typing import TypeVar, List, Generic

from pydantic import BaseModel, Field

from app.core.types import Token, Status

K = TypeVar("K")


class CredentialsAuthenticationWebsocket(BaseModel):
    access_token: Token | str = Field(..., title="Access token", alias='accessToken')


class StatusResponseWebSocket(BaseModel, Generic[K]):
    data: K | List[K] = Field(..., title="Data", alias='data')
    status: Status


class StatusMessageWebSocket(BaseModel):
    message: str
    status: Status


class CommandWebSocket(BaseModel):
    command: str
