from app.core.exception import UnauthorizedAccessException
from app.core.types import Token
from app.domain.services.user import AuthenticationCredentialsService
from app.infrastructure.repository.user import UserRepository
from app.presentation.schemes import UserResponse
from app.core.data import get_username


class AuthUseCase:
    def __init__(self):
        self.__auth_service = AuthenticationCredentialsService()

    async def login(self, code: int | str, password: str):
        token = await self.__auth_service.authenticate(
            get_username(code),
            password
        )

        return token

    async def logout(self, token: Token):
        return False

    async def check(self, token: Token):
        return await self.__auth_service.validate(token)

    async def get_user_profile(self, token: Token):
        status, user = await UserRepository.get_user_by_token(token)

        if not status:
            raise UnauthorizedAccessException()

        return UserResponse(
            code=user.code,
            firstname=user.firstname,
            maternal_surname=user.maternal_surname,
            paternal_surname=user.paternal_surname,
            email=user.email,
            role=user.role_value,
        )
