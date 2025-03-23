from app.core.exception import NotFoundException
from app.core.types import Token
from app.domain.services.auth import AuthenticationCredentialsService
from app.domain.services.user import UserService


class SessionUseCase:
    def __init__(self):
        self.__user_service = UserService()
        self.__auth_service = AuthenticationCredentialsService()

    async def get_current_user_session(self, token: Token):
        user = await self.__user_service.get_by_token(token)

        raise NotFoundException(detail="User not have session saved.")
