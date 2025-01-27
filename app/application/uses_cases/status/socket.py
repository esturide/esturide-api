import abc
import asyncio

from fastapi import HTTPException
from starlette.websockets import WebSocket

from app.core.types import Status, UUID
from app.domain.services.ride import RideService
from app.domain.services.travel import ScheduleService
from app.domain.services.user import AuthenticationCredentialsService
from app.presentation.schemes import UserResponse
from app.presentation.schemes.status import RideStatus, ListRides, RidesStatus, PassengerRideStatus, PassengerProfile
from app.presentation.schemes.websocket import CredentialsAuthenticationWebsocket, StatusMessageWebSocket, \
    StatusResponseWebSocket, CommandWebSocket


async def authentication_jwt_websocket(auth: AuthenticationCredentialsService, data):
    credentials = CredentialsAuthenticationWebsocket(**data)

    is_valid = await auth.validate(credentials.access_token)

    if not is_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid access token.",
        )

    return is_valid, credentials


async def get_user_from_token(auth: AuthenticationCredentialsService, data):
    credentials = CredentialsAuthenticationWebsocket(**data)

    user_found, user = await auth.get_user_from_token(credentials.access_token)

    if not user_found:
        raise HTTPException(
            status_code=401,
            detail="Invalid access token.",
        )

    return user


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

    @abc.abstractmethod
    async def notification(self, websocket: WebSocket, uuid: UUID): ...

    @abc.abstractmethod
    async def tracking(self, websocket: WebSocket): ...


class DriverEventsSocket(EventsSocketNotifications):
    async def notification(self, websocket: WebSocket, uuid: UUID):
        async def get_ride_status():
            rides = await self.ride_service.get_all_rides(schedule)
            passengers = await schedule.passengers.all()

            rides_response = []

            for r, p in zip(rides, passengers):
                user = PassengerProfile(
                    code=p.code,
                    firstname=p.firstname,
                    maternal_surname=p.maternal_surname,
                    paternal_surname=p.paternal_surname,
                )

                ride = PassengerRideStatus(
                    valid=r.validate,
                    cancel=r.cancel,
                    user=user
                )

                rides_response.append(ride)

            await websocket.send_json(StatusResponseWebSocket(
                data=RidesStatus(**{
                        'rides': rides_response,
                        'totalPassengers': await schedule.current_passengers,
                    }),
                status=Status.success,
            ).model_dump())

        await get_user_from_token(self.auth_service, await websocket.receive_json())

        status, schedule = await self.schedule_service.get(uuid)

        while True:
            await get_ride_status()

            await asyncio.sleep(5)

    async def tracking(self, websocket: WebSocket):
        user = await get_user_from_token(self.auth_service, await websocket.receive_json())


class PassengerEventsSocket(EventsSocketNotifications):
    async def notification(self, websocket: WebSocket, uuid: UUID):
        user = await get_user_from_token(self.auth_service, await websocket.receive_json())

    async def tracking(self, websocket: WebSocket):
        user = await get_user_from_token(self.auth_service, await websocket.receive_json())
