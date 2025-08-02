from typing import List

from pydantic import BaseModel, Field

from app.core.types import UUID
from app.presentation.schemes import TrackingRecord


class RideStatus(BaseModel):
    valid: bool
    cancel: bool


class PassengerProfile(BaseModel):
    code: int

    firstname: str = Field(..., alias='firstName')
    maternal_surname: str = Field(..., alias='maternalSurname')
    paternal_surname: str = Field(..., alias='paternalSurname')


class PassengerRideStatus(RideStatus):
    tracking: TrackingRecord = Field(TrackingRecord())
    user: PassengerProfile


class ScheduleStatus(BaseModel):
    ride_id: UUID = Field(..., alias='rideID')
    schedule_id: UUID = Field(..., alias='scheduleID')

    active: bool = False
    terminate: bool = False
    cancel: bool = False
    current_passengers: int = Field(..., alias='currentPassengers')

    ride: RideStatus


class ListRides(BaseModel):
    rides: List[RideStatus] = Field(..., alias='rides')
    total_passengers: int = Field(..., alias='totalPassengers')


class RidesStatus(BaseModel):
    rides: List[PassengerRideStatus] = Field(..., alias='rides')
    total_passengers: int = Field(..., alias='totalPassengers')
