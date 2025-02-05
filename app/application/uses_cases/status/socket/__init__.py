from app.core.manager import SessionSocket
from app.core.types import Status
from app.domain.services.auth import AuthenticationCredentialsService
from app.presentation.schemes.websocket import StatusMessageWebSocket


class EventsSocket:
    def __init__(self):
        self.__auth_service = AuthenticationCredentialsService()

    async def validate_token(self, session: SessionSocket):
        await session.get_user_from_token(self.__auth_service)

        await session.send_model(StatusMessageWebSocket(
            message="Token is valid.",
            status=Status.success
        ))
