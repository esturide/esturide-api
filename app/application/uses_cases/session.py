from app.core.exception import NotFoundException
from app.core.types import Token
from app.domain.services.ride import RideService
from app.domain.services.schedule import ScheduleService
from app.domain.services.travel import TravelService
from app.domain.services.user import UserService


class SessionUseCase:
    def __init__(self):
        self.user_service = UserService()
        self.schedule_service = ScheduleService()
        self.ride_service = RideService()
        self.travel_service = TravelService()

    async def get_restore_session(self, token: Token):
        user = await self.user_service.get_by_token(token)

        raise NotFoundException(detail="User not have session saved.")
