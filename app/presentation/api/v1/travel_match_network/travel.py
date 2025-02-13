from typing import List

from fastapi import APIRouter, HTTPException

from app.core.dependencies import DependScheduleCase, AuthUserCredentials
from app.core.types import UUID, Status
from app.presentation.schemes import StatusMessage
from app.presentation.schemes.travels import ScheduleTravel, TravelResult

travel = APIRouter(prefix="/travel", tags=["Travels"])


@travel.get("/search", response_model=List[TravelResult])
async def search_travel(schedule_case: DependScheduleCase, auth_user: AuthUserCredentials, limit: int = 16):
    return await schedule_case.get_all_travels(limit)


@travel.get("/", response_model=List[TravelResult])
async def get_all_travels(schedule_case: DependScheduleCase, auth_user: AuthUserCredentials, limit: int = 16):
    return await schedule_case.get_all_travels(limit)


@travel.post("/", response_model=StatusMessage)
async def schedule_new_travel(schedule: ScheduleTravel, schedule_case: DependScheduleCase,
                              auth_user: AuthUserCredentials):
    status = await schedule_case.create(schedule, auth_user)

    if not status:
        raise HTTPException(status_code=400)

    return {
        "status": Status.success,
        "message": "New schedule traveled successfully.",
    }


@travel.put("/{uuid}", response_model=StatusMessage)
async def edit_travel(uuid: UUID, schedule_case: DependScheduleCase, auth_user: AuthUserCredentials):

    return {
        "status": Status.success,
        "message": "Travel be changed."
    }


@travel.get("/{uuid}", response_model=TravelResult)
async def get_travel(uuid: UUID, schedule_case: DependScheduleCase, auth_user: AuthUserCredentials):
    return await schedule_case.get(uuid, auth_user)


@travel.delete("/cancel/{uuid}", response_model=StatusMessage)
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
