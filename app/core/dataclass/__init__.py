import dataclasses

from app.core.types import UUID

@dataclasses.dataclass
class DataDriverCurrentSession:
    schedule: UUID
    driver_to: UUID


@dataclasses.dataclass
class DataPassengerCurrentSession:
    schedule: UUID
    ride_to: UUID


DataSession = DataDriverCurrentSession | DataPassengerCurrentSession
