from fastapi import FastAPI

from app.core.types import Status
from app.presentation.api.v1.travel_match_network.auth_travel import auth_travel
from app.presentation.api.v1.travel_match_network.location import location
from app.presentation.api.v1.travel_match_network.ride import ride
from app.presentation.api.v1.travel_match_network.schedule.status.http import status_http
from app.presentation.api.v1.travel_match_network.schedule import schedule_travel
from app.presentation.schemes import StatusMessage

travels_match_network_v1 = FastAPI(title="Travel Match Network (μ) API")
travels_match_network_v1.include_router(ride)
travels_match_network_v1.include_router(schedule_travel)
travels_match_network_v1.include_router(status_http)
travels_match_network_v1.include_router(auth_travel)
travels_match_network_v1.include_router(location)


@travels_match_network_v1.get('/', response_model=StatusMessage)
async def index():
    return {
        'status': Status.success,
        'message': 'Everything is working!',
    }
