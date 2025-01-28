import asyncio

from app.application.uses_cases.status.socket.events import EventsSocketNotifications
from app.core.manager.socket import SessionSocket
from app.core.types import Status, UUID
from app.presentation.schemes.status import RidesStatus, PassengerRideStatus, PassengerProfile
from app.presentation.schemes.websocket import StatusResponseWebSocket, StatusMessageWebSocket


class DriverEventsSocket(EventsSocketNotifications):
    async def notification(self, session: SessionSocket, uuid: UUID):
        async def get_ride_status():
            status, schedule = await self.schedule_service.get(uuid)
            rides = await self.ride_service.get_all_rides(schedule)
            passengers = await schedule.passengers.all()

            rides_response = []

            for r, p in zip(rides, passengers):
                user = PassengerProfile(**{
                    'code': p.code,
                    'firstname': p.firstname,
                    'maternalSurname': p.maternal_surname,
                    'paternalSurname': p.paternal_surname,
                })

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

        async def tracking_user_gps(): ...

        await session.get_user_from_token(self.auth_service)

        await session.send_model(StatusMessageWebSocket(
            message="Token is valid.",
            status=Status.success
        ))

        while True:
            await get_ride_status()     # OUT
            await tracking_user_gps()   # IN

            await asyncio.sleep(5)

    async def tracking(self, session: SessionSocket):
        user = await session.get_user_from_token(self.auth_service)
