from typing import List

from fastapi import APIRouter

from app.core.dependencies import NominatimDepend
from app.core.exception import NotFoundException
from app.presentation.schemes.AddressLocation import FoundLocation

location = APIRouter(prefix="/location", tags=["Location"])


@location.get("/search", response_model=List[FoundLocation])
async def search_location(query: str, geolocator: NominatimDepend):
    def search_direction(direction: str):
        return geolocator.geocode(direction, exactly_one=False)

    results = search_direction(query)

    if not results:
        raise NotFoundException(
            detail="No results were found for the specified address."
        )

    founds = []

    for locations in results:
        founds.append({
            "address": locations.address,
            "latitude": locations.latitude,
            "longitude": locations.longitude
        })

    return founds
