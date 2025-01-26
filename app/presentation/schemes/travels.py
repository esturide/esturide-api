from pydantic import BaseModel, Field

from app.core.types import UUID


class TrackingRecord(BaseModel):
    location: str = ""
    latitude: str = "0.000000"
    longitude: str = "0.000000"


class ScheduleTravel(BaseModel):
    start: TrackingRecord
    end: TrackingRecord
    price: int
    max_passengers: int = 4


class TravelResult(BaseModel):
    uuid: UUID

    price: int
    active: bool = False
    terminate: bool = False
    cancel: bool = False
    max_passengers: int = Field(4, alias='maxPassengers')

    driver: DriverProfile

    origin: TrackingRecord
    destination: TrackingRecord