import typing

from pydantic import BaseModel, Field

from app.core.enum import CurrentRuleUser
from app.core.types import UUID, UserCode


class DriverCurrentSession(BaseModel):
    schedule: UUID
    driver_to: UUID = Field(..., alias='driverTo')


class PassengerCurrentSession(BaseModel):
    schedule: UUID
    ride_to: UUID = Field(..., alias='rideTo')


SessionType = typing.TypeVar(
    "SessionType", bound=typing.Union[DriverCurrentSession, PassengerCurrentSession, None]
)


class SessionResponse(BaseModel, typing.Generic[SessionType]):
    code: UserCode
    current_role: CurrentRuleUser = Field(..., alias='currentRole')
    current: SessionType = Field(..., alias='current')
