from typing import List

from pydantic import BaseModel, Field

class RideStatus(BaseModel):
    valid: bool
    cancel: bool


class ScheduleStatus(BaseModel):
    active: bool = False
    terminate: bool = False
    cancel: bool = False
    current_passengers: int = Field(..., alias='currentPassengers')

    ride: RideStatus


class ListRides(BaseModel):
    rides: List[RideStatus]
    total_passengers: int = Field(..., alias='totalPassengers')
