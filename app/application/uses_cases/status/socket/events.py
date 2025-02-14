import abc

from app.core.manager.sockets.session import SessionSocket
from app.core.types import UUID
from app.domain.services.auth import AuthenticationCredentialsService
from app.domain.services.ride import RideService
from app.domain.services.travel import ScheduleService


class EventsSocketNotifications:
    def __init__(self):
        self.schedule_service = ScheduleService()
        self.ride_service = RideService()
        self.auth_service = AuthenticationCredentialsService()

    @abc.abstractmethod
    async def pipeline(self, session: SessionSocket, uuid: UUID): ...
