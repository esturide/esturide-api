from app.application.uses_cases.status.socket.events import EventsSocketNotifications
from app.core.manager.socket import SessionSocket
from app.core.types import UUID


class PassengerEventsSocket(EventsSocketNotifications):
    async def pipeline(self, session: SessionSocket, uuid: UUID):
        user = await session.get_user_from_token(self.auth_service)
