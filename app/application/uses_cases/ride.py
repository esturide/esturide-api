from fastapi import HTTPException

from app.core.types import UUID, UserCode
from app.domain.models import User
from app.domain.services.ride import RideService
from app.domain.services.travel import ScheduleService
from app.presentation.schemes import RideRequest


class RideCase:
    def __init__(self):
        self.__ride_service = RideService()
        self.__schedule_service = ScheduleService()

    async def check_valid_ride(self, uuid: UUID, code: UserCode):
        status, schedule = await self.__schedule_service.get(uuid)

        if not status:
            raise HTTPException(status_code=404, detail="Travel schedule not found.")

        driver = await schedule.designated_driver

        if driver.code == code:
            raise HTTPException(status_code=400, detail="The driver cannot request the same trip that he had planned.")

        if not schedule.is_valid:
            raise HTTPException(status_code=400, detail="The travel is not valid.")

        if await schedule.current_passengers >= schedule.max_passenger:
            raise HTTPException(status_code=400, detail="The travel has reached the maximum number of occupants.")

        if any([
            code == passenger.code for passenger in await schedule.users
        ]):
            raise HTTPException(status_code=409, detail="The ride was previously requested.")

        return uuid, status, schedule, driver

    async def create(self, ride: RideRequest, code: UserCode):
        uuid, status, schedule, driver = await self.check_valid_ride(ride.travel_uuid, code)

        await self.__ride_service.create(schedule, ride, code)

        return True

    async def get_current_ride(self, code: UserCode) -> UUID:
        ride = await self.__ride_service.get_current_ride(code)

        return ride.uuid

    async def cancel(self, uuid: UUID, code: UserCode):
        status, schedule = await self.__schedule_service.get(uuid)

        if not status:
            raise HTTPException(status_code=404, detail="Travel schedule not found.")

        driver = await schedule.designated_driver

        if driver.code == code:
            raise HTTPException(status_code=400, detail="The driver cannot request the same trip that he had planned.")

        if not schedule.is_valid:
            raise HTTPException(status_code=400, detail="The travel is not valid.")

        return await self.__ride_service.cancel(schedule, code)

    async def get(self, uuid: UUID, code: UserCode):
        status, schedule = await self.__schedule_service.get(uuid)

        if not status:
            raise HTTPException(status_code=404, detail="Travel schedule not found.")

        await self.__ride_service.get(schedule, code)
