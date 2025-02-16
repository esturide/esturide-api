from fastapi import HTTPException

from app.core.types import UserCode, UUID
from app.domain.models import User, Schedule
from app.domain.types import LocationData
from app.infrastructure.repository.travels.ride import RideRepository
from app.infrastructure.repository.user import UserRepository


class RideService:
    async def set_tracking(self, uuid: UUID, tracking: LocationData) -> bool:
        ride = await RideRepository.get_by_uuid(uuid)
        status_ride = not ride.cancel and ride.validate

        if status_ride:
            await RideRepository.update_tracking(uuid, tracking)

        return status_ride

    async def create(self, schedule: Schedule, user: User):
        return await RideRepository.create(schedule, user)

    async def get_by_uuid(self, uuid: UUID):
        return await RideRepository.get_by_uuid(uuid)

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
