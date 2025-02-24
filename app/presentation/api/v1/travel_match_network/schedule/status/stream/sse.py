import asyncio
import json

from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
from starlette.responses import StreamingResponse

from app.core.dependencies import DependDriverEventsCase, DependPassengerEventsCase, AuthUserCredentials, \
    DependSEEConnectionManager
from app.core.types import UUID
from app.presentation.schemes.status import ListRides, ScheduleStatus

stream_sse = APIRouter(prefix="/stream", tags=["Streaming (SSE)"])


@stream_sse.get("/driver/{uuid}", response_model=ListRides)
async def events_notify_driver(uuid: UUID, events: DependDriverEventsCase, auth_user: AuthUserCredentials):
    return EventSourceResponse(await events.notify_sse(uuid, auth_user))


@stream_sse.get("/passenger/{uuid}", response_model=ScheduleStatus)
async def events_notify_passenger(uuid: UUID, events: DependPassengerEventsCase, auth_user: AuthUserCredentials):
    return EventSourceResponse(await events.notify_sse(uuid, auth_user))
