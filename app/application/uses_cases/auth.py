from app.core.types import Token
from app.domain.services.auth import AuthenticationCredentialsService


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
