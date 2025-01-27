from starlette.websockets import WebSocket

from app.core.types import Status
from app.domain.services.user import AuthenticationCredentialsService
from app.presentation.schemes.websocket import CredentialsAuthenticationWebsocket, StatusMessageWebSocket


class EventsSocket:
    def __init__(self):
        self.__auth_service = AuthenticationCredentialsService()

    async def echo(self, websocket: WebSocket):
        await websocket.accept()

        data = await websocket.receive_json()
        credentials = CredentialsAuthenticationWebsocket(**data)

        is_valid = await self.__auth_service.validate(credentials.access_token)

        if not is_valid:
            await websocket.send_json(StatusMessageWebSocket(
                message="Failure authenticating.",
                status=Status.failure
            ).model_dump())

            await websocket.close()

        await websocket.send_json(credentials.model_dump())
