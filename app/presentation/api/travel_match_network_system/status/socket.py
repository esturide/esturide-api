from fastapi import HTTPException, APIRouter
from starlette.websockets import WebSocket

from app.core.dependencies import DependEventsSocketCase
from app.core.types import Status
from app.presentation.schemes import StatusMessage
from app.presentation.schemes.websocket import StatusMessageWebSocket

status_socket = APIRouter(prefix="/socket", tags=["Status notify for WebSockets"])


@status_socket.get("/", response_model=StatusMessage)
async def index():
    return {
        'status': Status.success,
        'message': 'Everything is working!',
    }


@status_socket.websocket('/echo')
async def validate_token(websocket: WebSocket, events: DependEventsSocketCase):
    try:
        await events.validate_token(websocket)
    except HTTPException as e:
        await websocket.send_json(StatusMessageWebSocket(
            message=e.detail,
            status=Status.failure
        ).model_dump())
    finally:
        await websocket.close()
