from app.domain.models import User
from app.domain.services.ride import RideService
from app.domain.services.schedule import ScheduleService
from app.domain.services.travel import TravelService
from app.domain.services.user import UserService


class SessionService:
    def __init__(self):
        self.user_service = UserService()
        self.schedule_service = ScheduleService()
        self.ride_service = RideService()
        self.travel_service = TravelService()

    async def get_last_travel(self, user: User):
        pass

