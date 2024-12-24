from app.domain.models import User, Schedule, Rating

class RatingRepository:
    async def fetch_trip_and_user(self, user_id: str, schedule_id: str):
        try:
            user = await User.nodes.get(code=user_id)
            schedule = await Schedule.nodes.get(uuid=schedule_id)
            return user, schedule
        except Exception:
            return None, None

    async def save_rating(self, user, schedule, overall: int, punctuality: int, driving_behavior: int):
        rating = Rating(
            overall = overall,
            punctuality = punctuality,
            driving_behavior = driving_behavior
        )

        await rating.save()
        await user.rated.connect(rating)
        await schedule.rating.connect(rating)
