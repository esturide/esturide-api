import abc

from app.core.manager.socket import SessionSocket
from app.core.types import UUID
from app.domain.services.ride import RideService
from app.domain.services.travel import ScheduleService
from app.domain.services.user import AuthenticationCredentialsService


class EventsSocketNotifications:
    def __init__(self):
        self.schedule_service = ScheduleService()
        self.ride_service = RideService()
        self.auth_service = AuthenticationCredentialsService()

    @abc.abstractmethod
    async def notification(self, session: SessionSocket, uuid: UUID): ...

    @abc.abstractmethod
    async def tracking(self, session: SessionSocket): ...
