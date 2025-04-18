import abc
import asyncio

from fastapi import HTTPException
from pydantic import BaseModel
from starlette.websockets import WebSocket

from app.core.types import UUID
from app.domain.models import User
from app.domain.services.ride import RideService
from app.domain.services.schedule import ScheduleService
from app.presentation.schemes.status import RideStatus, ListRides, ScheduleStatus


def send_data_dump(model: BaseModel) -> str:
    return str(model.model_dump())


class EventsStatus:
    def __init__(self):
        self.schedule_service = ScheduleService()
        self.ride_service = RideService()

    @abc.abstractmethod
    async def notify_ws(self, uuid: UUID, websocket: WebSocket, user: User) -> bool: ...

    @abc.abstractmethod
    async def notify_sse(self, uuid: UUID, user: User): ...

    @abc.abstractmethod
    async def notify_http(self, uuid: UUID, user: User): ...


class DriverStatusCase(EventsStatus):
    async def notify_ws(self, uuid: UUID, websocket: WebSocket, user: User):
        status, schedule = await self.schedule_service.get_by_uuid(uuid)

        if not status:
            raise HTTPException(status_code=404, detail="Not Found")

        await websocket.accept()

        while True:
            await websocket.send_text(f"Notify to driver: {user}")
            await asyncio.sleep(1)

    async def notify_sse(self, uuid: UUID, user: User):
        async def event_generator():
            status, schedule = await self.schedule_service.get_by_uuid(uuid)

            if not status:
                raise HTTPException(status_code=404, detail="Travel schedule not found")

            while True:
                rides = await self.ride_service.get_all_rides(schedule)

                yield send_data_dump(
                    ListRides(**{
                        'rides': [
                            RideStatus(
                                valid=r.validate,
                                cancel=r.cancel,
                            ) for r in rides
                        ],
                        'totalPassengers': await schedule.current_passengers,
                    })
                )

                await asyncio.sleep(5)

        return event_generator()

    async def notify_http(self, uuid: UUID, user: User):
        status, schedule = await self.schedule_service.get_by_uuid(uuid)

        if not status:
            raise HTTPException(status_code=404, detail="Travel schedule not found.")

        rides = await self.ride_service.get_all_rides(schedule)

        return ListRides(**{
            'rides': [
                RideStatus(
                    valid=r.validate,
                    cancel=r.cancel,
                ) for r in rides
            ],
            'totalPassengers': await schedule.current_passengers,
        })


class UserStatusCase(EventsStatus):
    async def notify_ws(self, uuid: UUID, websocket: WebSocket, user: User):
        status, schedule = await self.schedule_service.get_by_uuid(uuid)

        if not status:
            raise HTTPException(status_code=404, detail="Not Found.")

        await websocket.accept()

        while True:
            await websocket.send_text(f"Notify to driver: {user}")
            await asyncio.sleep(1)

    async def notify_sse(self, uuid: UUID, user: User):
        async def event_generator():
            status, schedule = await self.schedule_service.get_by_uuid(uuid)

            if not status:
                raise HTTPException(status_code=404, detail="Travel schedule not found.")

            while True:
                ride = await self.ride_service.get(schedule, user)

                yield send_data_dump(
                    ScheduleStatus(**{
                        'active': schedule.active,
                        'terminate': schedule.finished,
                        'cancel': schedule.cancel,
                        'currentPassengers': await schedule.current_passengers,
                        'ride': RideStatus(
                            valid=ride.validate,
                            cancel=ride.cancel,
                        )
                    })
                )

                await asyncio.sleep(5)

        return event_generator()

    async def notify_http(self, uuid: UUID, user: User):
        schedule = await self.schedule_service.get_by_uuid_ride(uuid)
        ride = await self.ride_service.get_by_uuid(uuid)

        return ScheduleStatus(**{
            'rideID': uuid,
            'scheduleID': schedule.uuid,

            'active': schedule.active,
            'terminate': schedule.terminate,
            'cancel': schedule.cancel,

            'currentPassengers': await schedule.current_passengers,
            'ride': RideStatus(
                valid=ride.validate,
                cancel=ride.cancel,
            )
        })


class EventsTestingCase:
    async def echo(self, websocket: WebSocket):

        while True:
            received = await websocket.receive()

            await websocket.send_text(f"Echo: {received}")

    async def echo_auth(self, websocket: WebSocket):
        received = await websocket.receive()

        await websocket.send_text(f"Echo: {received}")

        while True:
            received = await websocket.receive()

            await websocket.send_text(f"Echo: {received}")
