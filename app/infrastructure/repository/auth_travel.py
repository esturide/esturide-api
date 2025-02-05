from app.domain.models import User, Schedule


class TravelRepository:
    async def fetch_travel_and_user(self, user_id: str, trip_id: str):
        try:
            user = await User.nodes.get(code=user_id)
            trip = await Schedule.nodes.get(uuid=trip_id)
            return user, trip
        except Exception as e:
            return None, None
