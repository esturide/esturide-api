from app.core.types import Token
from app.domain.services.user import AuthenticationCredentialsService
from app.infrastructure.repository.user import UserRepository
from app.presentation.schemes import UserResponse


class AuthUseCase:
    def __init__(self):
        self.__auth_service = AuthenticationCredentialsService()

    async def login(self, code: int | str, password: str):
        if isinstance(code, str):
            code = int(code)

        token = await self.__auth_service.authenticate(
            code,
            password
        )

        return token

    async def logout(self, token: Token):
        return {
            "status": "success",
        }

    async def check(self, token: Token):
        return await self.__auth_service.validate(token)

    async def get_user_profile(self, token: Token):
        status, user = await UserRepository.get_user_by_token(token)

        if not status:
            return {"status": "failed"}

        return UserResponse(
            code=user.code,
            firstname=user.firstname,
            maternal_surname=user.maternal_surname,
            paternal_surname=user.paternal_surname,
            email=user.email,
        )
