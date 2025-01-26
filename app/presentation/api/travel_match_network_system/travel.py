from typing import List

from fastapi import APIRouter, HTTPException

from app.core.dependencies import DependScheduleCase, AuthUserCredentials
from app.core.types import UUID
from app.presentation.schemes import ScheduleTravel, TravelResult

travel = APIRouter(prefix="/travel", tags=["Travels"])


@travel.get("/search")
async def search_travel(schedule_case: DependScheduleCase, auth_user: AuthUserCredentials, limit: int = 16) -> List[TravelResult]:
    return await schedule_case.get_all_travels(limit)


@travel.get("/")
async def get_all_travels(schedule_case: DependScheduleCase, auth_user: AuthUserCredentials, limit: int = 16) -> List[TravelResult]:
    return await schedule_case.get_all_travels(limit)


@travel.post("/")
async def schedule_new_travel(schedule: ScheduleTravel, schedule_case: DependScheduleCase,
                              auth_user: AuthUserCredentials):
    status = await schedule_case.create(schedule, auth_user)

    if not status:
        raise HTTPException(status_code=400)

    return {
        "status": "success",
    }


@travel.get("/{uuid}")
async def get_travel(uuid: UUID, schedule_case: DependScheduleCase, auth_user: AuthUserCredentials):
    return await schedule_case.get(uuid, auth_user)


@travel.delete("/cancel/{uuid}")
async def cancel_travel(uuid: UUID, schedule_case: DependScheduleCase, auth_user: AuthUserCredentials):
    status = await schedule_case.cancel(uuid, auth_user)

    return {
        "status": "success" if status else "failure",
    }
