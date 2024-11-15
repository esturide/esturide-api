from fastapi import HTTPException

from app.domain.services.user import UserService
from app.presentation.schemes import UserRequest, UserResponse, ProfileUpdateRequest


class UserUseCase:
    def __init__(self):
        self.__user_service = UserService()

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
        if not user_req.code > 100000000:
            raise HTTPException(status_code=401, detail="Invalid user code")

        status = await self.__user_service.create(user_req)

        if not status:
            raise HTTPException(status_code=400, detail="User no created")

        return status

    async def update(self, code: int, user_req: ProfileUpdateRequest, uuid_user_code: int):
        if uuid_user_code == code:
            status, _ = await self.__user_service.update(code, user_req)

            return status

        raise HTTPException(status_code=401, detail="Invalid credentials")

    async def delete(self, code: int, uuid_user_code: int, is_admin: bool):
        if uuid_user_code == code:
            return await self.__user_service.delete(code)

        raise HTTPException(status_code=401, detail="Invalid credentials")
