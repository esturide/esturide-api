from fastapi import HTTPException

from app.core.types import UUID, UserCode
from app.core.utils.scheme_json import create_travel_scheme
from app.domain.models import User
from app.domain.services.schedule import ScheduleService
from app.presentation.schemes.travels import ScheduleTravelRequest



class ScheduleCase:
    def __init__(self):
        self.__schedule_service = ScheduleService()

    async def create(self, schedule: ScheduleTravelRequest, driver: User):
        if not driver.is_driver:
            raise HTTPException(status_code=400, detail="You need become driver.")

        return await self.__schedule_service.create(schedule, driver)

    async def get_current_travel(self, code: UserCode):
        schedule = await self.__schedule_service.get_current_travel(code)
        driver = await schedule.designated_driver
        origin, destination = await schedule.path_routes

        return create_travel_scheme(schedule, driver, origin, destination)

    async def get(self, uuid: UUID, auth_user: User):
        status, schedule = await self.__schedule_service.get(uuid)

        if not status:
            raise HTTPException(status_code=404, detail="Not Found.")

        driver = await schedule.driver.single()
        origin, destination = await schedule.path_routes

        if not auth_user.code == driver.code:
            raise HTTPException(status_code=401, detail="Invalid code.")

        return create_travel_scheme(schedule, driver, origin, destination)

    async def get_all_travels(self, limit: int):
        schedules = []

        for schedule in await self.__schedule_service.get_all(limit):
            driver = await schedule.designated_driver
            origin, destination = await schedule.path_routes

            schedules.append(
                create_travel_scheme(schedule, driver, origin, destination)
            )

        return schedules

    async def cancel(self, uuid: UUID, auth_user: User):
        status, schedule = await self.__schedule_service.get(uuid)

        if not status:
            raise HTTPException(status_code=404, detail="Not Found.")

        driver = await schedule.designated_driver

        if not driver.code == auth_user.code:
            raise HTTPException(status_code=401, detail="Invalid code.")

        await self.__schedule_service.update(uuid, cancel=True)

        return status


    async def terminate(self, uuid: UUID, auth_user: User):
        status, schedule = await self.__schedule_service.get(uuid)

        if not status:
            raise HTTPException(status_code=404, detail="Not Found.")

        driver = await schedule.designated_driver

        if not driver.code == auth_user.code:
            raise HTTPException(status_code=401, detail="Invalid code.")

        await self.__schedule_service.update(uuid, terminate=True, active=False)

        return status
