from fastapi import APIRouter, HTTPException, Query
from sse_starlette.sse import EventSourceResponse
from starlette.websockets import WebSocket

from app.core.dependencies import DependDriverEventsCase, DependPassengerEventsCase, AuthUserCredentials, \
    DependEventsTestingCase
from app.core.types import UUID
from app.domain.credentials import get_user_credentials_header
from app.presentation.schemes.status import ListRides, ScheduleStatus

status = APIRouter(prefix="/status", tags=["Status notify"])


@status.websocket("/testing_echo")
async def ws_echo(websocket: WebSocket, events: DependEventsTestingCase):
    await websocket.accept()
    await events.echo(websocket)


@status.websocket("/testing_echo_auth")
async def ws_echo_auth(websocket: WebSocket, events: DependEventsTestingCase):
    await websocket.accept(subprotocol="auth-v1")

    try:
        token = await websocket.receive_text()

        status, user = await get_user_credentials_header({"access_token": f"{token}"})

        if not status:
            #raise HTTPException(status_code=401, detail="Token no found")
            await websocket.close(code=1008, reason="Token not found or invalid.")
            return

        while True:
            try:
                await events.echo(websocket)
            except Exception as e:
                print(f"WebSocket receive/send error: {e}")
                break

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close(code=1000, reason="Connection closed normally.")


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
