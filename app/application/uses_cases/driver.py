from app.core.enum import RoleUser
from app.core.types import UserCode, Token
from app.domain.services.driver import DriverService
from app.domain.services.user import UserService


class DriverUseCase:
    def __init__(self):
        self.__driver_service = DriverService()
        self.__user_service = UserService()

    async def set_user_driver(self, token: Token) -> bool:
        user = await self.__user_service.get_by_token(token)

        async with self.__user_service.save(user) as node:
            node.role_value = RoleUser.driver

        return True

    async def check_user_driver(self, code: UserCode) -> bool:
        user = await self.__user_service.get_by_code(code)

        return user.role_value == RoleUser.driver
