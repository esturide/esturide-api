import typing

from pydantic import BaseModel

from app.core.enum import RoleUser
from app.core.types import UserCode, UUID


class DriverCurrentSession(BaseModel):
    schedule: UUID


class PassengerCurrentSession(BaseModel):
    schedule: UUID
    ride: UUID


T = typing.TypeVar("T", bound=typing.Union[DriverCurrentSession, PassengerCurrentSession])

class SessionResponse(BaseModel, typing.Generic[T]):
    code: UserCode
    role: RoleUser
    current: T
