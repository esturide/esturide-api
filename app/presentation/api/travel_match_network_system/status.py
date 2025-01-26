from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse
from starlette.websockets import WebSocket

from app.core.dependencies import DependDriverEventsCase, DependPassengerEventsCase, AuthUserCredentials, \
    EventsTestingCase
from app.core.types import UUID
from app.domain.credentials import get_user_credentials_header
from app.presentation.schemes.status import ListRides, ScheduleStatus

status = APIRouter(prefix="/status", tags=["Status notify"])


@status.websocket("/testing_echo")
async def ws_echo(websocket: WebSocket, events: EventsTestingCase):
    await events.echo(websocket)


@status.websocket("/testing_echo")
async def ws_echo_auth(uuid: UUID, websocket: WebSocket, events: EventsTestingCase):
    status, user = await get_user_credentials_header(dict(websocket.headers))

    if not status:
        raise HTTPException(status_code=401, detail="Token no found")

    await events.echo(websocket)


@status.websocket("/driver/{uuid}")
async def notify_driver_status(uuid: UUID, websocket: WebSocket, events: DependDriverEventsCase):
    status, user = await get_user_credentials_header(dict(websocket.headers))

    if not status:
        raise HTTPException(status_code=401, detail="Access token not found")

    await events.notify_ws(uuid, websocket, user)


@status.websocket("/user/{uuid}")
async def notify_user_status(uuid: UUID, websocket: WebSocket, events: DependPassengerEventsCase):
    status, user = await get_user_credentials_header(dict(websocket.headers))

    if not status:
        raise HTTPException(status_code=401, detail="Access token not found")

    await events.notify_ws(uuid, websocket, user)


@status.get("/events/driver/{uuid}", response_model=ListRides)
async def events_notify_driver(uuid: UUID, events: DependDriverEventsCase, auth_user: AuthUserCredentials):
    return EventSourceResponse(await events.notify_events(uuid, auth_user))


@status.get("/events/passenger/{uuid}", response_model=ScheduleStatus)
async def events_notify_passenger(uuid: UUID, events: DependPassengerEventsCase, auth_user: AuthUserCredentials):
    return EventSourceResponse(await events.notify_events(uuid, auth_user))
