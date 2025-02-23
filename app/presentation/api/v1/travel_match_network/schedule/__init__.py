from typing import List

from fastapi import APIRouter

from app.core.dependencies import DependScheduleCase, AuthUserCredentials
from app.core.types import UUID, Status
from app.presentation.schemes import StatusMessage
from app.presentation.schemes.travels import ScheduleTravelRequest, TravelScheduleResponse, RideStatusResponse, \
    RideStatusRequest

schedule_travel = APIRouter(prefix="/schedule", tags=["Schedule travels"])


@schedule_travel.get("/search", response_model=List[TravelScheduleResponse])
async def search_travel(schedule_case: DependScheduleCase, auth_user: AuthUserCredentials, limit: int = 16):
    return await schedule_case.get_all_travels(limit)


@schedule_travel.get("/current", response_model=TravelScheduleResponse)
async def get_current_schedule(schedule_case: DependScheduleCase, auth_user: AuthUserCredentials):
    return await schedule_case.get_current_travel(auth_user.code)


@schedule_travel.post("/", response_model=StatusMessage)
async def schedule_new_travel(schedule: ScheduleTravelRequest, schedule_case: DependScheduleCase,
                              auth_user: AuthUserCredentials):
    status = await schedule_case.create(schedule, auth_user.code)

    if status:
        return {
            "status": Status.success,
            "message": "New schedule traveled successfully.",
        }

    return {
        "status": Status.failure,
        "message": "Cannot schedule new travel.",
    }


@schedule_travel.put("/{uuid}", response_model=StatusMessage)
async def edit_travel(uuid: UUID, schedule_case: DependScheduleCase, auth_user: AuthUserCredentials):
    return {
        "status": Status.success,
        "message": "Travel be changed."
    }


@schedule_travel.get("/{uuid}", response_model=TravelScheduleResponse)
async def get_travel(uuid: UUID, schedule_case: DependScheduleCase, auth_user: AuthUserCredentials):
    return await schedule_case.get(uuid, auth_user)


@schedule_travel.patch("/start/{uuid}", response_model=StatusMessage)
async def start_travel(uuid: UUID, schedule_case: DependScheduleCase, auth_user: AuthUserCredentials):
    status = await schedule_case.start(uuid, auth_user.code)

    if status:
        return {
            "status": Status.success,
            "message": "Travel is start."
        }
    else:
        return {
            "status": Status.failure,
            "message": "Travel can not be started."
        }


@schedule_travel.patch("/finished/{uuid}", response_model=StatusMessage)
async def finished_travel(uuid: UUID, schedule_case: DependScheduleCase, auth_user: AuthUserCredentials):
    status = await schedule_case.finished(uuid, auth_user.code)

    if status:
        return {
            "status": Status.success,
            "message": "Travel is finished."
        }
    else:
        return {
            "status": Status.failure,
            "message": "Travel can not be finished."
        }


@schedule_travel.patch("/cancel/{uuid}", response_model=StatusMessage)
async def cancel_travel(uuid: UUID, schedule_case: DependScheduleCase, auth_user: AuthUserCredentials):
    status = await schedule_case.cancel(uuid, auth_user.code)

    if status:
        return {
            "status": Status.success,
            "message": "Travel is cancel."
        }
    else:
        return {
            "status": Status.failure,
            "message": "Travel can not be cancelled."
        }


@schedule_travel.get("/passengers/{uuid}")
async def get_passengers_status(uuid: UUID, schedule_case: DependScheduleCase, auth_user: AuthUserCredentials) -> List[
    RideStatusResponse]:
    return await schedule_case.get_all_current_passengers(uuid)


@schedule_travel.patch("/passengers/{uuid}", response_model=StatusMessage)
async def set_passengers_status(uuid: UUID, ride: RideStatusRequest, schedule_case: DependScheduleCase,
                                auth_user: AuthUserCredentials):
    status = await schedule_case.valid_passenger(uuid, ride)

    if status:
        return {
            "status": Status.success,
            "message": "Changes to the ride have been accepted."
        }
    else:
        return {
            "status": Status.failure,
            "message": "Passengers can not be changed."
        }
