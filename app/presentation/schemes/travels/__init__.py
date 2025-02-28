from datetime import datetime, timedelta
from typing import List

from pydantic import BaseModel, Field, field_validator

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
    start: TrackingRecord = Field(TrackingRecord(), title="Location where the schedule begins", alias='start')
    end: TrackingRecord = Field(TrackingRecord(), title="Location where the schedule ends", alias='end')
    price: int = Field(5, title="Max passengers", alias='maxPassengers')
    max_passengers: int = Field(4, title="Max passengers", alias='maxPassengers')

    start_time: datetime = Field(default_factory=lambda: datetime.now(), title="Time starting", alias='startTime')
    end_time: datetime = Field(default_factory=lambda: datetime.now() + timedelta(minutes=30), title="Time finished", alias='endTime')

    @field_validator("start_time")
    def validate_start(cls, start):
        now = datetime.now()

        if start < now:
            raise ValueError("The start time must be equal to or later than the current time.")

        return start

    @field_validator("end_time")
    def validate_end(cls, end, values):
        start = values.get("startTime")

        if start is None:
            raise ValueError("No valid start time was provided for comparison.")

        if end <= start:
            raise ValueError("The end time must be after the start time.")

        if end - start < timedelta(minutes=30):
            raise ValueError("The difference between start and end must be greater than 30 minutes.")

        return end


class TravelScheduleResponse(BaseModel):
    uuid: UUID

    driver: DriverUser

    price: int
    active: bool = False
    terminate: bool = False
    cancel: bool = False
    max_passengers: int = Field(4, alias='maxPassengers')

    starting: datetime = Field(default_factory=lambda: datetime.now(), title="Time starting", alias='starting')
    finished: datetime = Field(default_factory=lambda: datetime.now() + timedelta(minutes=30), title="Time finished", alias='finished')

    @field_validator("starting")
    def validate_start(cls, start):
        now = datetime.now()

        if start < now:
            raise ValueError("The start time must be equal to or later than the current time.")

        return start

    @field_validator("finished")
    def validate_end(cls, end, values):
        start = values.get("start")

        if start is None:
            raise ValueError("No valid start time was provided for comparison.")

        if end <= start:
            raise ValueError("The end time must be after the start time.")

        if end - start < timedelta(minutes=30):
            raise ValueError("The difference between start and end must be greater than 30 minutes.")

        return end

    passengers: List[PassengerUser] = Field([], title="Passengers", alias='passengers')

    origin: TrackingRecord
    destination: TrackingRecord


class Tracking(BaseModel):
    uuid: UUID
    record: TrackingRecord


class RideStatusRequest(BaseModel):
    code: UserCode
    validate: bool = True


class RideStatusResponse(PassengerUser):
    validate: bool = True
