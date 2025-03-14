import asyncio

from fastapi import HTTPException

from app.core.types import UUID, UserCode
from app.domain.services.ride import RideService
from app.domain.services.schedule import ScheduleService
from app.domain.services.user import UserService
from app.domain.types import LocationData
from app.presentation.schemes import RideRequest
from app.presentation.schemes.status import RideStatus, ScheduleStatus
from app.presentation.schemes.travels import Tracking


class RideCase:
    def __init__(self):
        self.__user_service = UserService()
        self.__ride_service = RideService()
        self.__schedule_service = ScheduleService()

    async def set_tracking(self, tracking: Tracking, waiting_seconds: int = 5):
        uuid = tracking.uuid
        record = LocationData(**dict(tracking.record))

        await asyncio.sleep(waiting_seconds)

        status = await self.__ride_service.set_tracking(uuid, record)

        return status

    async def check_valid_ride(self, uuid: UUID, code: UserCode):
        schedule = await self.__schedule_service.get_by_uuid(uuid)

        driver = await schedule.designated_driver

        if driver.code == code:
            raise HTTPException(status_code=400, detail="The driver cannot request the same trip that he had planned.")

        if not schedule.is_valid:
            raise HTTPException(status_code=400, detail="The schedule is not valid.")

        if await schedule.current_passengers >= schedule.max_passenger:
            raise HTTPException(status_code=400, detail="The schedule has reached the maximum number of occupants.")

        if any([
            code == passenger.code for passenger in await schedule.users
        ]):
            raise HTTPException(status_code=409, detail="The ride was previously requested.")

        return uuid, schedule, driver

    async def create(self, ride: RideRequest, code: UserCode):
        uuid, schedule, driver = await self.check_valid_ride(ride.travel_uuid, code)
        status = schedule.valid_for_ride

        if status:
            user = await self.__user_service.get_by_code(code)

            await self.__ride_service.create(schedule, user)

        return status

    async def get_current_ride(self, code: UserCode, *args, **kwargs):
        ride = await self.__ride_service.get_current_ride(code, *args, **kwargs)

        return ride.uuid

    async def get_active_ride(self, code: UserCode) -> UUID:
        ride = await self.__ride_service.get_active_ride(code)

        return ride.uuid

    async def get_current_ride_from_user(self, code: UserCode):
        ride = await self.__ride_service.get_active_ride(code)
        schedule = await self.__schedule_service.get_by_uuid_ride(ride.uuid)

        return ScheduleStatus(**{
            'rideID': ride.uuid,
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

    async def cancel(self, uuid: UUID, code: UserCode):
        schedule = await self.__schedule_service.get_by_uuid(uuid)

        driver = await schedule.designated_driver

        if driver.code == code:
            raise HTTPException(status_code=400, detail="The driver cannot request the same trip that he had planned.")

        if not schedule.is_valid:
            raise HTTPException(status_code=400, detail="The schedule is not valid.")

        return await self.__ride_service.set_cancel(schedule, code, True)

    async def get(self, uuid: UUID, code: UserCode):
        schedule = await self.__schedule_service.get_by_uuid(uuid)

        await self.__ride_service.get(schedule, code)
