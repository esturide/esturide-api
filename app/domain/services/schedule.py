from fastapi import HTTPException

from app.core.types import UUID, UserCode
from app.domain.models import User, Schedule
from app.infrastructure.repository.travels.schedule import ScheduleRepository, LocationData
from app.presentation.schemes.travels import ScheduleTravelRequest


class ScheduleService:
    def __init__(self):
        pass

    async def get_all(self, limit: int):
        return [
            schedule for schedule, travel, user in await ScheduleRepository.filter_ordered_time(limit)
        ]

    async def get(self, uuid: UUID):
        return await ScheduleRepository.get(uuid=uuid)

    async def get_current_travel(self, code: UserCode) -> Schedule:
        return await ScheduleRepository.get_active_travel(code)

    async def create(self, schedule: ScheduleTravelRequest, driver: User):
        start = schedule.start
        end = schedule.end

        last_schedule = await ScheduleRepository.filter_last_travels_by_driver(driver.code)

        if not all([schedule.terminate or schedule.cancel for schedule in last_schedule]):
            raise HTTPException(
                status_code=400,
                detail="You can schedule a new travel, if you do not cancel or finish the last travel."
            )

        status, _ = await ScheduleRepository.create(
            driver.code,
            schedule.max_passengers,
            schedule.price,
            LocationData(
                start.location,
                start.latitude,
                start.longitude,
            ),
            LocationData(
                end.location,
                end.latitude,
                end.longitude,
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
