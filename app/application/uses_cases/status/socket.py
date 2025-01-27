from fastapi import HTTPException
from starlette.websockets import WebSocket

from app.core.types import Status
from app.domain.services.user import AuthenticationCredentialsService
from app.presentation.schemes.websocket import CredentialsAuthenticationWebsocket, StatusMessageWebSocket


class EventsSocket:
    def __init__(self):
        self.__auth_service = AuthenticationCredentialsService()

    async def validate_token(self, websocket: WebSocket):
        await websocket.accept()

        data = await websocket.receive_json()
        credentials = CredentialsAuthenticationWebsocket(**data)

        is_valid = await self.__auth_service.validate(credentials.access_token)

        if not is_valid:
            raise HTTPException(
                status_code=401,
                detail="Invalid access token.",
            )

        await websocket.send_json(StatusMessageWebSocket(
            message="Token is valid.",
            status=Status.success
        ).model_dump())
