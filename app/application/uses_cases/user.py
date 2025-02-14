from fastapi import HTTPException

from app.core.enum import RoleUser
from app.core.types import Token, UserCode
from app.domain.services.auth import AuthenticationCredentialsService
from app.domain.services.user import UserService
from app.infrastructure.repository.user import UserRepository
from app.presentation.schemes import UserRequest, UserResponse, ProfileUpdateRequest


class UserUseCase:
    def __init__(self):
        self.__user_service = UserService()
        self.__auth_service = AuthenticationCredentialsService()

    async def get(self, code: int):
        status, user = await self.__user_service.get_by_code(code)

        if not status:
            raise HTTPException(status_code=404, detail="User not found")

        return UserResponse(
            code=user.code,
            firstname=user.firstname,
            maternal_surname=user.maternal_surname,
            paternal_surname=user.paternal_surname,
            email=user.email
        )

    async def create(self, user_req: UserRequest):
        if not user_req.code > 1000:
            raise HTTPException(status_code=401, detail="Invalid user code.")

        status = await self.__user_service.create(user_req)

        if not status:
            raise HTTPException(status_code=400, detail="User no created.")

        return status

    async def update(self, code: UserCode, user_req: ProfileUpdateRequest, uuid_user_code: UserCode):
        if uuid_user_code == code:
            status, _ = await self.__user_service.update(code, user_req)

            return status

        raise HTTPException(status_code=401, detail="Invalid credentials.")

    async def delete(self, code: UserCode, uuid_user_code: UserCode, is_admin: bool):
        if uuid_user_code == code or is_admin:
            return await self.__user_service.delete(code)

        raise HTTPException(status_code=401, detail="Invalid credentials.")

    async def get_user_role(self, token: Token) -> RoleUser:
        if not await self.__auth_service.validate(token):
            raise HTTPException(status_code=404, detail="Invalid credentials.")

        status, user = await UserRepository.get_user_by_token(token)

        if not status:
            raise HTTPException(status_code=404, detail="User not found.")

        return user.role_value
