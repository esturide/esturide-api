from fastapi import HTTPException

from app.core import settings
from app.core.oauth2 import encode, check_if_expired, secure_decode, decode
from app.core.types import Token, UserCode
from app.infrastructure.repository.user import UserRepository


class AuthenticationCredentialsService:
    def __init__(self):
        self.__user_repository = UserRepository()

    async def authenticate(self, code: UserCode, password: str) -> Token:
        status, user = await self.__user_repository.get_user_by_code(code)

        if not status:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials.",
            )

        if not user.same_password(password):
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials.",
            )

        data = {
            "code": user.code,
            "role": user.role_value,
            "is_validate": user.is_validate,
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

        return False

    async def refresh(self, token: Token) -> Token:
        decode_data = decode(token)
        status, user = await self.__user_repository.get_user_by_code(decode_data.get("code"))

        if not status:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials.",
            )

        data = {
            "code": user.code,
            "role": user.role_value,
            "is_validate": user.is_validate,
        }

        return encode(
            data, settings.access_token_expire_minutes
        )

    async def get_user_from_token(self, token: Token):
        if not check_if_expired(token):
            return False, None

        with secure_decode(token) as decoded:
            if code := decoded.get("code"):
                return await self.__user_repository.get_user_by_code(code)

        return False, None
