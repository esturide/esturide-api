from app.infrastructure.repository.rate import RatingRepository


class RatingService:
    def __init__(self):
        self.repository = RatingRepository()

    async def rate_trip(self, user_id: str, schedule_id: str, overall: int, punctuality: int, driving_behavior: int):
        user, schedule = await self.repository.fetch_trip_and_user(user_id, schedule_id)

        if not user or not schedule:
            raise ValueError("Invalid user or trip")

        if user not in await schedule.passengers.all():
            raise ValueError("User did not participate in this trip")

        if not schedule.finished:
            raise ValueError("Trip is not completed")

        await self.repository.save_rating(user, schedule, overall, punctuality, driving_behavior)
