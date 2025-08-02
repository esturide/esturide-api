from fastapi import HTTPException

from app.domain.models import User, Schedule
from app.infrastructure.repository.ride import RideData, RideRepository
from app.infrastructure.repository.travels.schedule import ScheduleRepository
from app.infrastructure.repository.user import UserRepository
from app.presentation.schemes import RideRequest


class RideService:
    def __init__(self):
        self.__schedule_repository = ScheduleRepository()
        self.__user_repository = UserRepository()
        self.__ride_repository = RideRepository()

    async def create(self, schedule: Schedule, ride: RideRequest, user: User):
        status = await self.__ride_repository.create(
            schedule,
            RideData(
                location=ride.origin.location,
                latitude=ride.origin.latitude,
                longitude=ride.origin.longitude,
            ),
            user
        )

        return status

    async def get(self, schedule: Schedule, user: User):
        status, ride = await self.__ride_repository.get(schedule, user)

        if not status:
            raise HTTPException(status_code=404, detail="Ride not found")

        return ride

    async def get_all_rides(self, schedule: Schedule):
        return await self.__ride_repository.get_all(schedule)
