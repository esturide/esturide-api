import typing

from fastapi import WebSocket, HTTPException

from app.domain.models import User
from app.domain.services.auth import AuthenticationCredentialsService
from app.presentation.schemes.websocket import CredentialsAuthenticationWebsocket

C = typing.TypeVar("C")


class SessionSocket(typing.Generic[C]):
    def __init__(self, ws: WebSocket) -> None:
        self.__websocket = ws

    async def send_model(self, model: C):
        await self.__websocket.send_json(model.model_dump())

    async def receive_model(self, model_class: typing.Type[C]):
        data = await self.__websocket.receive_json()

        return model_class(**data)

    async def get_user_from_token(self, auth: AuthenticationCredentialsService) -> User:
        data = await self.__websocket.receive_json()
        credentials = CredentialsAuthenticationWebsocket(**data)

        user_found, user = await auth.get_user_from_token(credentials.access_token)

        if not user_found:
            raise HTTPException(
                status_code=401,
                detail="Invalid access token.",
            )
        else:
            return user

    @property
    def websocket(self) -> WebSocket:
        return self.__websocket
