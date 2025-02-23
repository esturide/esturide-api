from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.dependencies import AuthUserCredentials

tracking = APIRouter(
    prefix="/tracking",
    tags=["Tracking"]
)

@tracking.websocket("/ws")
async def websocket_tracking(websocket: WebSocket ):
    await websocket.accept() 
    try:
        while True:
            data = await websocket.receive_text()
            response = f"Datos de tracking recibidos: {data}"
            await websocket.send_text(response)  
    except WebSocketDisconnect:
        print("El cliente se ha desconectado")
