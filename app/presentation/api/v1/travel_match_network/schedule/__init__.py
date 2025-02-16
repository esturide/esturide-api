from typing import List

from fastapi import APIRouter, HTTPException

from app.core.dependencies import DependScheduleCase, AuthUserCredentials
from app.core.types import UUID, Status
from app.presentation.schemes import StatusMessage
from app.presentation.schemes.travels import ScheduleTravelRequest, TravelScheduleResponse

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
    status = await schedule_case.create(schedule, auth_user)

    if not status:
        raise HTTPException(status_code=400)

    return {
        "status": Status.success,
        "message": "New schedule traveled successfully.",
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


@schedule_travel.delete("/{uuid}", response_model=StatusMessage)
async def cancel_travel(uuid: UUID, schedule_case: DependScheduleCase, auth_user: AuthUserCredentials):
    status = await schedule_case.cancel(uuid, auth_user)

    if status:
        return {
            "status": Status.success,
            "message": "Travel be cancelled."
        }
    else:
        return {
            "status": Status.failure,
            "message": "Travel can not be cancelled."
        }


@schedule_travel.patch("/{uuid}", response_model=StatusMessage)
async def finished_travel(uuid: UUID, schedule_case: DependScheduleCase, auth_user: AuthUserCredentials):
    status = await schedule_case.terminate(uuid, auth_user)

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
