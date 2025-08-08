import dataclasses
import datetime

from app.core.types import UUID


@dataclasses.dataclass
class DataSession:
    schedule: UUID
    connection: UUID

    active: bool
    finished: bool

    last_time_access: datetime.datetime
