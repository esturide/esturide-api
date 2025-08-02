from typing import List

from fastapi import HTTPException

from app.core.enum import StatusTravel
from app.core.exception import InvalidRequestException, NotFoundException, BadRequestException
from app.core.types import UUID
from app.core.utils.scheme_json import create_travel_scheme
from app.domain.models import User
from app.domain.services.ride import RideService
from app.domain.services.schedule import ScheduleService
from app.domain.services.travel import TravelService
from app.domain.services.user import UserService
from app.presentation.schemes import TrackingRecord
from app.presentation.schemes.travels import ScheduleTravelRequest, TravelScheduleResponse, RideStatusRequest, \
    RideStatusResponse


class ScheduleCase:
    def __init__(self):
        self.user_service = UserService()
        self.schedule_service = ScheduleService()
        self.ride_service = RideService()
        self.travel_service = TravelService()

    async def create(self, schedule: ScheduleTravelRequest, driver: int) -> bool:
        driver = await self.user_service.get_by_code(driver)

        if not driver.is_driver:
            raise NotFoundException(detail="You need become driver.")

        if len(schedule.seats) > schedule.max_passengers:
            raise BadRequestException(detail="Seats exceed.")

        status = await self.schedule_service.create(schedule, driver)

        if status:
            schedule = await self.schedule_service.get_current_travel(driver.code)
            travel = await self.travel_service.get(schedule, driver.code)

            """
            async with self.user_service.save(driver) as user:
                user.push_session(DataDriverCurrentSession(
                    schedule=schedule.uuid,
                    driver_to=travel.uuid
                ))
            """

        return status

    async def get_ride_tracking(self, user_code: int):
        schedule = await self.schedule_service.get_current_travel(user_code)
        users = await schedule.users

        for user in users:
            ride = await self.ride_service.get(schedule, user.code)
            tracking = await self.ride_service.get_last_tracking_position(ride.uuid)

            yield user, tracking

    async def get_current_travel(self, user_code: int) -> TravelScheduleResponse:
        schedule = await self.schedule_service.get_current_travel(user_code)
        driver = await schedule.designated_driver
        origin, destination = await schedule.path_routes

        return create_travel_scheme(schedule, driver, origin, destination,
                                    [(user, tracking) async for user, tracking in self.get_ride_tracking(user_code)])

    async def get(self, uuid: UUID, auth_user: User) -> TravelScheduleResponse:
        schedule = await self.schedule_service.get_by_uuid(uuid)

        driver = await schedule.driver.single()
        origin, destination = await schedule.path_routes

        if not auth_user.code == driver.code:
            raise HTTPException(status_code=401, detail="Invalid code.")

        return create_travel_scheme(schedule, driver, origin, destination,
                                    [(user, tracking) async for user, tracking in self.get_ride_tracking(driver.code)])

    async def get_all_travels(self, limit: int) -> List[TravelScheduleResponse]:
        schedules = []

        for schedule in await self.schedule_service.get_all(limit):
            if not schedule.valid_for_ride:
                continue

            driver = await schedule.designated_driver
            origin, destination = await schedule.path_routes

            schedules.append(
                create_travel_scheme(schedule, driver, origin, destination,
                                     [(user, tracking) async for user, tracking in self.get_ride_tracking(driver.code)])
            )

        return schedules

    async def set_status(self, uuid: UUID, user_code: int, status: StatusTravel):
        async def match_status(status: StatusTravel):
            all_status = {
                StatusTravel.start: not (schedule.cancel or schedule.terminate),
                StatusTravel.cancel: schedule.active or (not schedule.cancel and not schedule.terminate),
                StatusTravel.terminate: schedule.active or not schedule.cancel
            }

            match status:
                case StatusTravel.start:
                    if not (schedule.cancel or schedule.terminate):
                        await self.schedule_service.set_active(uuid)
                case StatusTravel.cancel:
                    if schedule.active or (not schedule.cancel and not schedule.terminate):
                        await self.schedule_service.set_cancel(uuid)
                case StatusTravel.terminate:
                    if schedule.active or not schedule.cancel:
                        await self.schedule_service.set_terminate(uuid)

            for status_type, cond in all_status.items():
                if status_type == status and cond:
                    return True

            return False

        schedule = await self.schedule_service.get_by_uuid(uuid)
        driver = await schedule.designated_driver

        if not driver.code == user_code:
            raise InvalidRequestException(detail="Invalid user code.")

        return await match_status(status)

    async def start(self, uuid: UUID, user_code: int):
        schedule = await self.schedule_service.get_by_uuid(uuid)
        driver = await schedule.designated_driver

        if not driver.code == user_code:
            raise InvalidRequestException(detail="Invalid user code.")

        can_start = not (schedule.cancel or schedule.terminate)

        if can_start:
            await self.schedule_service.set_active(uuid)

        return can_start

    async def finished(self, uuid: UUID, user_code: int):
        schedule = await self.schedule_service.get_by_uuid(uuid)
        driver = await schedule.designated_driver

        if not driver.code == user_code:
            raise InvalidRequestException(detail="Invalid user code.")

        can_finished = schedule.active or not schedule.cancel

        if can_finished:
            await self.schedule_service.set_terminate(uuid)

        return can_finished

    async def cancel(self, uuid: UUID, user_code: int):
        schedule = await self.schedule_service.get_by_uuid(uuid)
        driver = await schedule.designated_driver

        if not driver.code == user_code:
            raise InvalidRequestException(detail="Invalid user code.")

        can_finished = schedule.active or (not schedule.cancel and not schedule.terminate)

        if can_finished:
            await self.schedule_service.set_cancel(uuid)

        return can_finished

    async def valid_passenger(self, uuid: UUID, ride_status: RideStatusRequest) -> bool:
        schedule = await self.schedule_service.get_by_uuid(uuid)
        ride = await self.ride_service.get_active_ride(ride_status.code)

        if not ride.validate:
            return await self.ride_service.set_validate(schedule, ride_status.code, ride_status.validate)

        return False

    async def get_all_current_passengers(self, uuid: UUID) -> List[RideStatusResponse]:
        ride_status_responses = []
        schedule = await self.schedule_service.get_by_uuid(uuid)

        for passenger, ride in await self.ride_service.get_current_rides(schedule):
            position = await self.ride_service.get_last_tracking_position(ride.uuid)

            print(position)

            ride_status_responses.append(
                RideStatusResponse(
                    code=passenger.code,
                    firstname=passenger.firstname,
                    maternalSurname=passenger.maternal_surname,
                    paternalSurname=passenger.paternal_surname,
                    validate=ride.validate,
                    position=TrackingRecord(
                        latitude=position.latitude,
                        longitude=position.longitude,
                    )
                )
            )

        return ride_status_responses
