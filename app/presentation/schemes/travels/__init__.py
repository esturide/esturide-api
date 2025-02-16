from typing import List

from pydantic import BaseModel, Field

from app.core.types import UUID, UserCode
from app.presentation.schemes import TrackingRecord


class DriverUser(BaseModel):
    code: UserCode

    firstname: str
    maternal_surname: str = Field(..., title="Maternal surname", alias='maternalSurname')
    paternal_surname: str = Field(..., title="Paternal surname", alias='paternalSurname')
    position: TrackingRecord = Field(TrackingRecord(), title="Current position", alias='position')


class PassengerUser(BaseModel):
    code: UserCode

    firstname: str
    maternal_surname: str = Field(..., title="Maternal surname", alias='maternalSurname')
    paternal_surname: str = Field(..., title="Paternal surname", alias='paternalSurname')
    position: TrackingRecord = Field(TrackingRecord(), title="Current position", alias='position')


class ScheduleTravelRequest(BaseModel):
    start: TrackingRecord = Field(TrackingRecord(), title="Location where the travel begins", alias='start')
    end: TrackingRecord = Field(TrackingRecord(), title="Location where the travel ends", alias='end')
    price: int = Field(5, title="Max passengers", alias='maxPassengers')
    max_passengers: int = Field(4, title="Max passengers", alias='maxPassengers')


class TravelScheduleResponse(BaseModel):
    uuid: UUID

    driver: DriverUser

    price: int
    active: bool = False
    terminate: bool = False
    cancel: bool = False
    max_passengers: int = Field(4, alias='maxPassengers')

    passengers: List[PassengerUser] = Field([], title="Passengers", alias='passengers')

    origin: TrackingRecord
    destination: TrackingRecord


class Tracking(BaseModel):
    uuid: UUID
    record: TrackingRecord
