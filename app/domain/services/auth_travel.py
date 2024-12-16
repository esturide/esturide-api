from app.infrastructure.repository.auth_travel import TravelRepository

class AuthService:
    def __init__(self):
        self.repository = TravelRepository()


    async def validate_trip_auth(self, user_id: str, trip_id: str) -> bool:
        user, trip = await self.repository.fetch_travel_and_user(user_id, trip_id)


        if not user or not trip:
            return False

        if user in await trip.passengers or user == await trip.designated_driver:
            return trip.is_valid and not trip.cancel and not trip.terminate

        return False
