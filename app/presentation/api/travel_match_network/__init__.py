from fastapi import FastAPI

from app.core.types import Status
from app.presentation.api.travel_match_network.ride import ride
from app.presentation.api.travel_match_network.status import status
from app.presentation.api.travel_match_network.status.socket import status_socket
from app.presentation.api.travel_match_network.travel import travel
from app.presentation.api.travel_match_network.auth_travel import auth_travel
from app.presentation.schemes import StatusMessage

travels_match_network = FastAPI(title="Travel Match Network System (μ) API")
travels_match_network.include_router(ride)
travels_match_network.include_router(travel)
travels_match_network.include_router(status)
travels_match_network.include_router(status_socket)
travels_match_network.include_router(auth_travel)


@travels_match_network.get('/', response_model=StatusMessage)
async def index():
    return {
        'status': Status.success,
        'message': 'Everything is working!',
    }
