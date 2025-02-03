from fastapi import HTTPException

from app.core import settings
from app.core.oauth2 import encode, check_if_expired, secure_decode
from app.core.types import Token
from app.infrastructure.repository.user import UserRepository
from app.presentation.schemes import UserRequest, ProfileUpdateRequest


class AuthenticationCredentialsService:
    def __init__(self):
        self.__user_repository = UserRepository()

    async def authenticate(self, code: int, password: str) -> Token:
        status, user = await self.__user_repository.get_user_by_code(code)

        if not status:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials.",
            )

        if user.password != password:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials.",
            )

        data = {
            "code": user.code
        }

        return encode(
            data, settings.access_token_expire_minutes
        )

    async def validate(self, token: Token):
        if not check_if_expired(token):
            return False

        with secure_decode(token) as decoded:
            if code := decoded.get("code"):
                status, user = await self.__user_repository.get_user_by_code(code)
                return status

        return True

    async def get_user_from_token(self, token: Token):
        if not check_if_expired(token):
            return False

        with secure_decode(token) as decoded:
            if code := decoded.get("code"):
                return await self.__user_repository.get_user_by_code(code)

        return False, None


class UserService:
    def __init__(self):
        self.__user_repository = UserRepository()

    async def get_by_code(self, user_code: int):
        return await self.__user_repository.get_user_by_code(user_code)

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

    async def update(self, code: int, user_req: ProfileUpdateRequest):
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

    async def delete(self, code: int):
        return await self.__user_repository.delete(code)
