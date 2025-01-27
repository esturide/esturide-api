from fastapi import HTTPException
from starlette.websockets import WebSocket

from app.core.types import Status
from app.domain.services.ride import RideService
from app.domain.services.travel import ScheduleService
from app.domain.services.user import AuthenticationCredentialsService
from app.presentation.schemes.websocket import CredentialsAuthenticationWebsocket, StatusMessageWebSocket


async def authentication_jwt_websocket(auth: AuthenticationCredentialsService, data):
    credentials = CredentialsAuthenticationWebsocket(**data)

    is_valid = await auth.validate(credentials.access_token)

    if not is_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid access token.",
        )

    return is_valid


class EventsSocket:
    def __init__(self):
        self.__auth_service = AuthenticationCredentialsService()

    async def validate_token(self, websocket: WebSocket):
        await authentication_jwt_websocket(self.__auth_service, await websocket.receive_json())

        await websocket.send_json(StatusMessageWebSocket(
            message="Token is valid.",
            status=Status.success
        ).model_dump())


class EventsSocketNotifications:
    def __init__(self):
        self.schedule_service = ScheduleService()
        self.ride_service = RideService()
        self.auth_service = AuthenticationCredentialsService()


class DriverEventsSocket(EventsSocketNotifications):
    async def notification(self, websocket: WebSocket):
        await authentication_jwt_websocket(self.auth_service, await websocket.receive_json())


class PassengerEventsSocket(EventsSocketNotifications):
    async def notification(self, websocket: WebSocket):
        await authentication_jwt_websocket(self.auth_service, await websocket.receive_json())

    async def tracking(self, websocket: WebSocket):
        await authentication_jwt_websocket(self.auth_service, await websocket.receive_json())
