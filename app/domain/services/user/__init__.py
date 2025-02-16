import contextlib

from app.core.exception import FailureSaveDataException, NotFoundException
from app.core.types import Token, UserCode
from app.domain.models import User
from app.infrastructure.repository.user import UserRepository
from app.presentation.schemes import UserRequest, ProfileUpdateRequest


class UserService:
    def __init__(self):
        self.__user_repository = UserRepository()

    async def get_by_code(self, code: UserCode) -> User:
        status, user = await self.__user_repository.get_user_by_code(code)

        if not status:
            raise NotFoundException(detail="User not found.")

        return user

    async def get_by_token(self, token: Token) -> User:
        status, user = await self.__user_repository.get_user_by_token(token)

        if not status:
            raise NotFoundException(detail="User not found.")

        return user

    async def create(self, user_req: UserRequest):
        status, user = await self.__user_repository.create(
            user_req.code,
            user_req.firstname,
            user_req.maternal_surname,
            user_req.paternal_surname,
            user_req.curp,
            user_req.birth_date,
            user_req.email,
            user_req.password.get_secret_value(),
        )

        return status

    async def update(self, code: UserCode, user_req: ProfileUpdateRequest):
        status, user = await self.__user_repository.update(
            code,
            user_req.firstname,
            user_req.maternal_surname,
            user_req.paternal_surname,
            user_req.curp,
            user_req.birth_date,
            user_req.email,
            user_req.password.get_secret_value(),
        )

        return status, user

    @contextlib.asynccontextmanager
    async def save(self, user: User):
        yield user

        status = await self.__user_repository.save(user)

        if not status:
            raise FailureSaveDataException()

    async def delete(self, code: UserCode):
        return await self.__user_repository.delete(code)
