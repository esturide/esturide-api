import contextlib

from fastapi import HTTPException, WebSocket, WebSocketDisconnect

from app.core.exception import ResponseException
from app.core.manager.sockets.session import SessionSocket
from app.core.types import Status
from app.presentation.schemes.websocket import StatusMessageWebSocket


class SocketConnectionManager:
    def __init__(self):
        pass

    @contextlib.asynccontextmanager
    async def session(self, websocket: WebSocket):
        await websocket.accept()

        try:
            yield SessionSocket(websocket)
        except WebSocketDisconnect:
            await websocket.close()
        except HTTPException | ResponseException as e:
            await websocket.send_json(StatusMessageWebSocket(
                message=e.detail,
                status=Status.failure
            ).model_dump())
        except Exception as e:
            await websocket.send_json(StatusMessageWebSocket(
                message="Maybe something went wrong.",
                status=Status.failure
            ).model_dump())
            raise e
        finally:
            await websocket.close()
