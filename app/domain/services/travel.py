from fastapi import HTTPException

from app.core.exception import NotFoundException
from app.core.types import UUID
from app.domain.models import User, Schedule, Travel
from app.domain.types import LocationData
from app.infrastructure.repository.auth_travel import TravelRepository
from app.infrastructure.repository.travels.schedule import ScheduleRepository
from app.infrastructure.repository.user import UserRepository
from app.presentation.schemes import ScheduleTravel


class ScheduleService:
    def __init__(self):
        self.__schedule_repository = ScheduleRepository()

    async def get_all(self, limit: int):
        return [
            schedule for schedule, travel, user in await self.__schedule_repository.filter_ordered_time(limit)
        ]

    async def get(self, uuid: UUID):
        return await self.__schedule_repository.get(uuid=uuid)

    async def create(self, schedule: ScheduleTravel, driver: User):
        start = schedule.start
        end = schedule.end

        last_schedule = await self.__schedule_repository.filter_last_travels_by_driver(driver.code)

        if not all([schedule.terminate or schedule.cancel for schedule in last_schedule]):
            raise HTTPException(
                status_code=400,
                detail="You can schedule a new travel, if you do not cancel or finish the last travel"
            )

        status, _ = await self.__schedule_repository.create(
            driver.code,
            schedule.max_passengers,
            schedule.price,
            LocationData(
                start.location,
                start.latitude,
            ),
            LocationData(
                end.location,
                end.latitude,
            )
        )

        return True

    async def update(self, uuid: UUID, active: bool | None = None, terminate: bool | None = None,
                     cancel: bool | None = None):
        status, schedule = await self.get(uuid)

        if not status:
            return False

        schedule.active = active if active is not None else schedule.active
        schedule.terminate = terminate if terminate is not None else schedule.terminate
        schedule.cancel = cancel if cancel is not None else schedule.cancel

        await schedule.save()

        return status


class TravelService:
    async def get(self, schedule: Schedule, code: int) -> Travel:
        _, user = await UserRepository.get_user_by_code(code)

        if user is None:
            raise NotFoundException("Driver not found.")

        return await TravelRepository.get(schedule, user)
