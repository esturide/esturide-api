from fastapi import HTTPException

from app.core.types import UUID
from app.domain.models import User
from app.domain.services.ride import RideService
from app.domain.services.travel import ScheduleService
from app.presentation.schemes import RideRequest


class RideCase:
    def __init__(self):
        self.__ride_service = RideService()
        self.__schedule_service = ScheduleService()

    async def create(self, ride: RideRequest, user: User):
        uuid = ride.travel_uuid
        status, schedule = await self.__schedule_service.get(uuid)

        if not status:
            raise HTTPException(status_code=404, detail="Travel schedule not found")

        driver = await schedule.designated_driver
        if driver.code == user.code:
            raise HTTPException(status_code=400, detail="The driver cannot request the same trip that he had planned")

        if not schedule.is_valid:
            raise HTTPException(status_code=400, detail="The travel is not valid")

        if await schedule.current_passengers >= schedule.max_passenger:
            raise HTTPException(status_code=400, detail="The travel has reached the maximum number of occupants")

        if any([
            user.code == passenger.code for passenger in await schedule.user_management_system
        ]):
            raise HTTPException(status_code=409, detail="The ride was previously requested")

        await self.__ride_service.create(
            schedule,
            ride,
            user
        )

        return True

    async def get(self, uuid: UUID, user: User):
        status, schedule = await self.__schedule_service.get(uuid)

        if not status:
            raise HTTPException(status_code=404, detail="Travel schedule not found")

        await self.__ride_service.get(schedule, user)
