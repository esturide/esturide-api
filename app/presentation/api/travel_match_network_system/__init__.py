from fastapi import FastAPI

from app.presentation.api.travel_match_network_system.ride import ride
from app.presentation.api.travel_match_network_system.status import status
from app.presentation.api.travel_match_network_system.travel import travel

travels = FastAPI(title="Travel Match Network System (μ) API")
travels.include_router(ride)
travels.include_router(travel)
travels.include_router(status)


@travels.get('/')
async def index():
    return {
        "status": "ok",
    }
