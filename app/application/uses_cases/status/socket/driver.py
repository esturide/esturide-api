import asyncio

from app.application.uses_cases.status.socket.events import EventsSocketNotifications
from app.core.manager.socket import SessionSocket
from app.core.types import Status, UUID
from app.presentation.schemes.status import RidesStatus, PassengerRideStatus, PassengerProfile
from app.presentation.schemes.websocket import StatusResponseWebSocket, StatusMessageWebSocket


class DriverEventsSocket(EventsSocketNotifications):
    async def get_ride_status(self, session: SessionSocket, uuid: UUID):
        while True:
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

            await asyncio.sleep(1)

    async def tracking_user_gps(self, session: SessionSocket, uuid: UUID):
        while True:
            echo = await session.websocket.receive_text()
            await session.websocket.send_text(f"{echo}")

            await asyncio.sleep(1)

    async def pipeline(self, session: SessionSocket, uuid: UUID):
        await session.get_user_from_token(self.auth_service)

        await session.send_model(StatusMessageWebSocket(
            message="Token is valid.",
            status=Status.success
        ))

        send_task = asyncio.create_task(self.get_ride_status(session, uuid))
        receive_task = asyncio.create_task(self.tracking_user_gps(session, uuid))

        await asyncio.gather(send_task, receive_task)
