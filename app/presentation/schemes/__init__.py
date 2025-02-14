import datetime
from typing import List, TypeVar, Generic

from pydantic import BaseModel, Field, field_validator, SecretStr, EmailStr

from app.core.enum import RoleUser
from app.core.types import UUID, Status, UserCode

T = TypeVar('T')


class StatusResponse(BaseModel, Generic[T]):
    data: List[T] | T
    status: Status = Field(..., title="Status response")


class StatusMessage(BaseModel):
    status: Status = Field(..., title="Status response")
    message: str = Field(..., title="Message response")


class UserRequest(BaseModel):
    code: UserCode

    firstname: str
    maternal_surname: str
    paternal_surname: str
    curp: str = Field(..., title="CURP", alias='curp')
    birth_date: datetime.date = Field(..., title="Birth date", description="The user's birth date")

    email: EmailStr = Field(..., title="Email", alias='email')
    password: SecretStr

    @field_validator('birth_date')
    def check_age(cls, birth_date):
        today = datetime.date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        if age < 18:
            raise ValueError('The person must be over 18 years old')

        return birth_date


class UserResponse(BaseModel):
    code: UserCode

    firstname: str
    maternal_surname: str
    paternal_surname: str

    email: EmailStr = Field(..., title="Email", alias='email')

    role: RoleUser = RoleUser.not_verified


class ProfileUpdateRequest(BaseModel):
    firstname: str
    maternal_surname: str
    paternal_surname: str
    curp: str
    birth_date: datetime.date

    email: EmailStr = Field(..., title="Email", alias='email')
    password: SecretStr


class DriverProfile(BaseModel):
    code: UserCode

    firstname: str
    maternal_surname: str
    paternal_surname: str


class AutomobileProfile(BaseModel):
    brand: str
    year: str
    model: int


class TrackingRecord(BaseModel):
    location: float = 0
    latitude: float = 0
    longitude: float = 0


class RideRequest(BaseModel):
    origin: TrackingRecord
    travel_uuid: UUID = Field(..., alias='UUID')


class AuthTravelRequest(BaseModel):
    user_id: str
    trip_id: str


class RateRequest(BaseModel):
    user_id: str
    schedule_id: str
    overall: int = Field(..., ge=1, le=5)
    punctuality: int = Field(..., ge=1, le=5)
    driving_behavior: int = Field(..., ge=1, le=5)


class AutomobileRequest(BaseModel):
    code: int
    brand: str
    year: int
    model: str


class AutomobileResponse(BaseModel):
    code: int
    brand: str
    year: int
    model: str
