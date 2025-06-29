from app.domain.services.rate import RatingService


async def rate_trip(user_id: str, schedule_id: str, overall: int, punctuality: int, driving_behavior: int):
    service = RatingService()
    await service.rate_trip(user_id, schedule_id, overall, punctuality, driving_behavior)
