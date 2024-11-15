from fastapi import APIRouter

from app.core.dependencies import AuthUserCredentials, DependRideCase
from app.core.types import UUID
from app.presentation.schemes import RideRequest

ride = APIRouter(prefix="/ride", tags=["Rides"])


@ride.post("/")
async def request_new_ride(ride_req: RideRequest, ride_case: DependRideCase, auth_user: AuthUserCredentials):
    status = await ride_case.create(ride_req, auth_user)

    return {
        "status": "success" if status else "failure"
    }


@ride.delete("/cancel/{uuid}")
async def cancel_ride(uuid: UUID, ride_case: DependRideCase, auth_user: AuthUserCredentials):
    return {
        "status": "success",
    }
