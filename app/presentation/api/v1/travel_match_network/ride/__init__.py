from fastapi import APIRouter

from app.core.dependencies import AuthUserCredentials, DependRideCase, DependPassengerEventsCase, \
    AuthUserCodeCredentials
from app.core.types import UUID, Status
from app.presentation.schemes import RideRequest, StatusResponse, StatusMessage
from app.presentation.schemes.status import ScheduleStatus
from app.presentation.schemes.travels import Tracking

ride = APIRouter(prefix="/ride", tags=["Request rides"])


@ride.post("/", response_model=StatusMessage)
async def request_new_ride(ride_req: RideRequest, ride_case: DependRideCase, auth_user: AuthUserCodeCredentials):
    status = await ride_case.create(ride_req, auth_user)

    if status:
        return {
            "status": Status.success,
            "message": "Ride is created."
        }
    else:
        return {
            "status": Status.failure,
            "message": "Ride cannot be created."
        }


@ride.get("/", response_model=ScheduleStatus)
async def get_current_ride_by_user(ride_case: DependRideCase, auth_user: AuthUserCredentials):
    return await ride_case.get_current_ride_from_user(auth_user.code)


@ride.delete("/", response_model=StatusMessage)
async def cancel_ride(ride_case: DependRideCase, auth_user: AuthUserCredentials):
    uuid = await ride_case.get_active_ride(auth_user.code)
    status = await ride_case.cancel(uuid, auth_user.code)

    if status:
        return {
            "status": Status.success,
            "message": "Ride is cancel."
        }
    else:
        return {
            "status": Status.failure,
            "message": "Ride cannot be cancel."
        }


@ride.post("/tracking", response_model=StatusMessage)
async def update_tracking(ride_case: DependRideCase, tracking: Tracking, auth_user: AuthUserCredentials):
    status = await ride_case.set_tracking(tracking)

    if status:
        return {
            "status": Status.success,
            "message": "GPS position updated."
        }
    else:
        return {
            "status": Status.failure,
            "message": "Failed to update GPS position."
        }
