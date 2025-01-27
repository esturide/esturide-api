from typing import List

from pydantic import BaseModel, Field

from app.presentation.schemes import TrackingRecord


class RideStatus(BaseModel):
    valid: bool
    cancel: bool


class PassengerProfile(BaseModel):
    code: int

    firstname: str
    maternal_surname: str
    paternal_surname: str


class PassengerRideStatus(RideStatus):
    tracking: TrackingRecord = Field(TrackingRecord())
    user: PassengerProfile


class ScheduleStatus(BaseModel):
    active: bool = False
    terminate: bool = False
    cancel: bool = False
    current_passengers: int = Field(..., alias='currentPassengers')

    ride: RideStatus


class ListRides(BaseModel):
    rides: List[RideStatus]
    total_passengers: int = Field(..., alias='totalPassengers')


class RidesStatus(BaseModel):
    rides: List[PassengerRideStatus]
    total_passengers: int = Field(..., alias='totalPassengers')
