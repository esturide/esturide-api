from fastapi import HTTPException

from app.core.types import UUID
from app.domain.models import User, Schedule
from app.infrastructure.repository.travels.schedule import ScheduleRepository, LocationData
from app.presentation.schemes.travels import ScheduleTravelRequest


class ScheduleService:
    async def get_all(self, limit: int):
        return [
            schedule for schedule, travel, user in await ScheduleRepository.filter_ordered_time(limit)
        ]

    async def get_by_uuid(self, uuid: UUID) -> Schedule:
        schedule = await ScheduleRepository.get(uuid=uuid)

        return schedule

    async def get_by_uuid_ride(self, uuid: UUID) -> Schedule:
        return await ScheduleRepository.get_from_uuid_ride(uuid)

    async def get_current_travel(self, code: int) -> Schedule:
        return await ScheduleRepository.get_active_travel(code)

    async def create(self, schedule: ScheduleTravelRequest, driver: User):
        start = schedule.start
        end = schedule.end

        last_schedule = await ScheduleRepository.filter_last_travels_by_driver(driver.code)

        if not all([schedule.terminate or schedule.cancel for schedule in last_schedule]):
            raise HTTPException(
                status_code=400,
                detail="You can schedule a new schedule, if you do not cancel or finish the last schedule."
            )

        status, _ = await ScheduleRepository.create(
            driver.code,
            schedule.max_passengers,
            schedule.price,
            LocationData(
                start.latitude,
                start.longitude,
            ),
            LocationData(
                end.latitude,
                end.longitude,
            ),
            schedule.starting,
            schedule.finished,
            schedule.seats
        )

        return status

    async def set_status(self, uuid: UUID, active: bool | None = None, terminate: bool | None = None,
                         cancel: bool | None = None) -> bool:
        schedule = await self.get_by_uuid(uuid)

        schedule.active = active if active is not None else schedule.active
        schedule.terminate = terminate if terminate is not None else schedule.terminate
        schedule.cancel = cancel if cancel is not None else schedule.cancel

        await schedule.save()

        return True

    async def set_cancel(self, uuid: UUID):
        schedule = await self.get_by_uuid(uuid)
        schedule.cancel = True

        await schedule.save()

        return True

    async def set_active(self, uuid: UUID):
        schedule = await self.get_by_uuid(uuid)
        schedule.active = True

        await schedule.save()

        return True

    async def set_terminate(self, uuid: UUID):
        schedule = await self.get_by_uuid(uuid)
        schedule.terminate = True

        await schedule.save()

        return True
