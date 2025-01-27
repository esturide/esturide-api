from fastapi import HTTPException, APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.core.dependencies import DependEventsSocketCase, DependDriverEventsSocketCase, DependPassengerEventsSocketCase
from app.core.types import Status, UUID
from app.presentation.schemes import StatusMessage
from app.presentation.schemes.websocket import StatusMessageWebSocket

status_socket = APIRouter(prefix="/socket", tags=["Status notify for WebSockets"])


@status_socket.get("/", response_model=StatusMessage)
async def index():
    return {
        'status': Status.success,
        'message': 'Everything is working!',
    }


@status_socket.websocket('/token')
async def validate_token(websocket: WebSocket, events: DependEventsSocketCase):
    await websocket.accept()

    try:
        await events.validate_token(websocket)
    except WebSocketDisconnect:
        await websocket.close()
    except HTTPException as e:
        await websocket.send_json(StatusMessageWebSocket(
            message=e.detail,
            status=Status.failure
        ).model_dump())
    finally:
        await websocket.close()


@status_socket.websocket('/driver/{uuid}')
async def validate_token(uuid: UUID, websocket: WebSocket, events: DependDriverEventsSocketCase):
    await websocket.accept()

    try:
        await events.notification(websocket, uuid)
    except WebSocketDisconnect:
        await websocket.close()
    except HTTPException as e:
        await websocket.send_json(StatusMessageWebSocket(
            message=e.detail,
            status=Status.failure
        ).model_dump())
    except Exception:
        await websocket.send_json(StatusMessageWebSocket(
            message="Maybe something went wrong.",
            status=Status.failure
        ).model_dump())
    finally:
        await websocket.close()


@status_socket.websocket('/passenger/{uuid}')
async def validate_token(uuid: UUID, websocket: WebSocket, events: DependPassengerEventsSocketCase):
    await websocket.accept()

    try:
        await events.notification(websocket, uuid)
    except WebSocketDisconnect:
        await websocket.close()
    except HTTPException as e:
        await websocket.send_json(StatusMessageWebSocket(
            message=e.detail,
            status=Status.failure
        ).model_dump())
    except Exception:
        await websocket.send_json(StatusMessageWebSocket(
            message="Maybe something went wrong.",
            status=Status.failure
        ).model_dump())
    finally:
        await websocket.close()
