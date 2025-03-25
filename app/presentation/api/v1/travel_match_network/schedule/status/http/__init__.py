from fastapi import APIRouter

from app.core.dependencies import AuthUserCodeCredentials, DependDriverEventsCase, DependPassengerEventsCase
from app.core.types import UUID
from app.presentation.schemes.status import ListRides, ScheduleStatus

status_http = APIRouter(prefix="/status", tags=["Status notify events"])


@status_http.get("/driver/{uuid}", response_model=ListRides)
async def events_notify_driver(uuid: UUID, events: DependDriverEventsCase, auth_user: AuthUserCodeCredentials):
    return await events.notify_http(uuid, auth_user)


@status_http.get("/passenger/{uuid}", response_model=ScheduleStatus)
async def events_notify_passenger(uuid: UUID, events: DependPassengerEventsCase, auth_user: AuthUserCodeCredentials):
    return await events.notify_http(uuid, auth_user)
