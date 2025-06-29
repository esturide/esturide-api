from app.domain.services.auth_travel import AuthService

async def authenticate_trip(user_id: str, trip_id: str) -> bool:
    service = AuthService()
    return await service.validate_trip_auth(user_id, trip_id)
