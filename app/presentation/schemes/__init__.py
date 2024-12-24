import datetime
import enum
from typing import List

from pydantic import BaseModel, Field, field_validator

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

    @field_validator('birth_date')
    def check_age(cls, birth_date):
        today = datetime.date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        if age < 18:
            raise ValueError('The person must be over 18 years old')

        return birth_date


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
    valid: bool
    cancel: bool


class ScheduleStatus(BaseModel):
    active: bool = False
    terminate: bool = False
    cancel: bool = False
    current_passengers: int

    ride: RideStatus


class ListRides(BaseModel):
    rides: List[RideStatus]
    total_passengers: int


class AuthTravelRequest(BaseModel):
    user_id: str
    trip_id: str



class RateRequest(BaseModel):
    user_id: str
    schedule_id: str
    overall: int = Field(..., ge=1, le=5)
    punctuality: int = Field(..., ge=1, le=5)
    driving_behavior: int = Field(..., ge=1, le=5)

