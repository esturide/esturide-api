from app.core.exception import UnauthorizedAccessException
from app.core.types import Token, UserCode
from app.domain.services.auth import AuthenticationCredentialsService
from app.infrastructure.repository.user import UserRepository
from app.presentation.schemes import UserResponse
from app.core.data import get_username


class AuthUseCase:
    def __init__(self):
        self.__auth_service = AuthenticationCredentialsService()

    async def login(self, code: UserCode, password: str):
        token = await self.__auth_service.authenticate(
            code,
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
            maternalSurname=user.maternal_surname,
            paternalSurname=user.paternal_surname,
            email=user.email,
            role=user.role_value,
        )

    async def refresh(self, token: Token):
        return await self.__auth_service.refresh(token)
