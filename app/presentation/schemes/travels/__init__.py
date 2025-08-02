from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.core.types import UUID
from app.presentation.schemes import TrackingRecord


class DriverUser(BaseModel):
    code: int

    firstname: str
    maternal_surname: str = Field(..., title="Maternal surname", alias='maternalSurname')
    paternal_surname: str = Field(..., title="Paternal surname", alias='paternalSurname')
    position: TrackingRecord = Field(TrackingRecord(), title="Current position", alias='position')


class PassengerUser(BaseModel):
    code: int

    firstname: str
    maternal_surname: str = Field(..., title="Maternal surname", alias='maternalSurname')
    paternal_surname: str = Field(..., title="Paternal surname", alias='paternalSurname')
    position: TrackingRecord = Field(TrackingRecord(), title="Current position", alias='position')


class ScheduleTravelRequest(BaseModel):
    start: TrackingRecord = Field(TrackingRecord(), title="Location where the schedule begins", alias='start')
    end: TrackingRecord = Field(TrackingRecord(), title="Location where the schedule ends", alias='end')
    price: int = Field(5, title="Price of travel", alias='price')

    starting: datetime = Field(..., title="Time starting", alias='starting')
    finished: datetime = Field(..., title="Time finished", alias='finished')

    max_passengers: int = Field(4, title="Max passengers", alias='maxPassengers')
    seats: List[str] = Field(['A', 'B', 'C'], title="All seats", alias='seats')


class TravelScheduleResponse(BaseModel):
    uuid: UUID

    driver: DriverUser

    price: int
    active: bool = False
    terminate: bool = False
    cancel: bool = False

    starting: datetime = Field(..., title="Time starting", alias='starting')
    finished: datetime = Field(..., title="Time finished", alias='finished')

    max_passengers: int = Field(4, alias='maxPassengers')
    seats: List[str] = Field(['A', 'B', 'C'], title="All seats", alias='seats')
    passengers: List[PassengerUser] = Field([], title="Passengers", alias='passengers')

    origin: TrackingRecord
    destination: TrackingRecord


class Tracking(BaseModel):
    uuid: UUID
    record: TrackingRecord


class RideStatusRequest(BaseModel):
    code: int
    validate: bool = True


class RideStatusResponse(PassengerUser):
    validate: bool = True
