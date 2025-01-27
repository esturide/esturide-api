from fastapi import FastAPI

from app.core.types import Status
from app.presentation.api.travel_match_network_system.ride import ride
from app.presentation.api.travel_match_network_system.status import status
from app.presentation.api.travel_match_network_system.status.socket import status_socket
from app.presentation.api.travel_match_network_system.travel import travel
from app.presentation.api.travel_match_network_system.auth_travel import auth_travel
from app.presentation.schemes import StatusMessage

travels = FastAPI(title="Travel Match Network System (μ) API")
travels.include_router(ride)
travels.include_router(travel)
travels.include_router(status)
travels.include_router(status_socket)
travels.include_router(auth_travel)


@travels.get('/', response_model=StatusMessage)
async def index():
    return {
        'status': Status.success,
        'message': 'Everything is working!',
    }
