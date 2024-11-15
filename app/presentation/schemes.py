import datetime
import enum
from typing import List

from pydantic import BaseModel

from app.core.types import UUID


class AccessCredential(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RoleUser(str, enum.Enum):
    not_verified = 'not_verified'
    user = 'user'
    admin = 'admin'
    staff = 'staff'
    student = 'student'


class UserRequest(BaseModel):
    code: int

    firstname: str
    maternal_surname: str
    paternal_surname: str
    curp: str
    birth_date: datetime.date

    email: str
    password: str


class UserResponse(BaseModel):
    code: int

    firstname: str
    maternal_surname: str
    paternal_surname: str

    email: str

    role: RoleUser = RoleUser.not_verified


class ProfileUpdateRequest(BaseModel):
    firstname: str
    maternal_surname: str
    paternal_surname: str
    curp: str
    birth_date: datetime.date

    email: str
    password: str


class DriverProfile(BaseModel):
    code: int

    firstname: str
    maternal_surname: str
    paternal_surname: str


class AutomobileProfile(BaseModel):
    brand: str
    year: str
    model: int


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
    max_passengers: int = 4

    driver: DriverProfile

    origin: TrackingRecord
    destination: TrackingRecord


class RideRequest(BaseModel):
    origin: TrackingRecord
    travel_uuid: UUID


class RideStatus(BaseModel):
    validate: bool
    cancel: bool


class ListRides(BaseModel):
    rides: List[RideStatus]
    total_passengers: int
