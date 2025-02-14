from fastapi import HTTPException

from app.core.types import UserCode
from app.domain.models import User, Schedule
from app.domain.types import RideData
from app.infrastructure.repository.travels.ride import RideRepository
from app.infrastructure.repository.travels.schedule import ScheduleRepository
from app.infrastructure.repository.user import UserRepository
from app.presentation.schemes import RideRequest


class RideService:
    def __init__(self):
        pass

    async def create(self, schedule: Schedule, ride: RideRequest, user: User):
        status = await RideRepository.create(
            schedule,
            RideData(
                location=ride.origin.location,
                latitude=ride.origin.latitude,
                longitude=ride.origin.longitude,
            ),
            user
        )

        return status

    async def get(self, schedule: Schedule, code: UserCode):
        status, user = await UserRepository.get_user_by_code(code)

        if not status:
            raise HTTPException(status_code=404, detail="Passenger not found.")

        status, ride = await RideRepository.get(schedule, user)

        if not status:
            raise HTTPException(status_code=404, detail="Ride not found.")

        return ride

    async def get_all_rides(self, schedule: Schedule):
        return await RideRepository.get_all(schedule)

    async def get_current_ride(self, code: UserCode):
        return await RideRepository.get_active_ride(code)

    async def cancel(self, schedule: Schedule, code: UserCode):
        status, user = await UserRepository.get_user_by_code(code)

        if not status:
            raise HTTPException(status_code=404, detail="Passenger not found.")

        status, ride = await RideRepository.get(schedule, user)

        if not status:
            raise HTTPException(status_code=404, detail="Ride not found.")

        ride.cancel = True
        await ride.save()

        return status
