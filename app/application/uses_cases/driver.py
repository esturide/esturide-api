from fastapi import HTTPException
from app.domain.services.driver import DriverService
from app.presentation.schemes import UserRequest, UserResponse, ProfileUpdateRequest


class DriverUseCase:
    def __init__(self):
        self.__driver_service = DriverService()

    async def get(self, code: int):
        status, driver = await self.__driver_service.get_by_code(code)

        if not status:
            raise HTTPException(status_code=404, detail="Driver not found")

        return UserResponse(
            code=driver.code,
            firstname=driver.firstname,
            maternal_surname=driver.maternal_surname,
            paternal_surname=driver.paternal_surname,
            email=driver.email,
        )

    async def create(self, driver_req: UserRequest):
        if not driver_req.code > 100000000:
            raise HTTPException(status_code=401, detail="Invalid driver code")

        response = await self.__driver_service.create(driver_req)

        return response

    async def delete(self, code: int, uuid_user_code: int):
        if uuid_user_code == code:
            return await self.__driver_service.delete(code)

        raise HTTPException(status_code=401, detail="Invalid credentials")
