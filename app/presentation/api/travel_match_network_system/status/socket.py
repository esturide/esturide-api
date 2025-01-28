from fastapi import APIRouter, WebSocket

from app.core.dependencies import DependEventsSocketCase, DependDriverEventsSocketCase, DependPassengerEventsSocketCase, \
    DependSocketConnectionManager
from app.core.types import Status, UUID
from app.presentation.schemes import StatusMessage

status_socket = APIRouter(prefix="/socket", tags=["Status notify for WebSockets"])


@status_socket.get("/", response_model=StatusMessage)
async def index():
    return {
        'status': Status.success,
        'message': 'Everything is working!',
    }


@status_socket.websocket('/token')
async def validate_token(websocket: WebSocket, events: DependEventsSocketCase, manager: DependSocketConnectionManager):
    async with manager.session(websocket) as session:
        await events.validate_token(session)


@status_socket.websocket('/driver/{uuid}')
async def driver_notifications(uuid: UUID, websocket: WebSocket, events: DependDriverEventsSocketCase, manager: DependSocketConnectionManager):
    async with manager.session(websocket) as session:
        await events.notification(session, uuid)


@status_socket.websocket('/passenger/{uuid}')
async def passenger_notifications(uuid: UUID, websocket: WebSocket, events: DependPassengerEventsSocketCase, manager: DependSocketConnectionManager):
    async with manager.session(websocket) as session:
        await events.notification(session, uuid)
