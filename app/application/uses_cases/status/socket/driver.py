import asyncio

from app.application.uses_cases.status.socket.events import EventsSocketNotifications
from app.core.manager.socket import SessionSocket
from app.core.types import Status, UUID
from app.presentation.schemes.status import RidesStatus, PassengerRideStatus, PassengerProfile
from app.presentation.schemes.websocket import StatusResponseWebSocket


class DriverEventsSocket(EventsSocketNotifications):
    async def notification(self, session: SessionSocket, uuid: UUID):
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

            await session.send_model(StatusResponseWebSocket(
                data=RidesStatus(**{
                    'rides': rides_response,
                    'totalPassengers': await schedule.current_passengers,
                }),
                status=Status.success,
            ))

        await session.get_user_from_token(self.auth_service)

        status, schedule = await self.schedule_service.get(uuid)

        while True:
            await get_ride_status()

            await asyncio.sleep(5)

    async def tracking(self, session: SessionSocket):
        user = await session.get_user_from_token(self.auth_service)
