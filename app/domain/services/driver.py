from fastapi import HTTPException

from app.infrastructure.repository.driver import DriverRepository
from app.presentation.schemes import UserRequest


class DriverService:
    def __init__(self):
        self.__driver_repository = DriverRepository()

    async def get_by_code(self, driver_code: int):
        return await self.__driver_repository.get_driver_by_code(driver_code)

    async def create(self, user_req: UserRequest):
        status, user = await self.__driver_repository.create_or_update(
            code=user_req.code,
            firstname=user_req.firstname,
            maternal_surname=user_req.maternal_surname,
            paternal_surname=user_req.paternal_surname,
            curp=user_req.curp,
            birth_date=user_req.birth_date,
            email=user_req.email,
            password=user_req.password,
        )

        if not status:
            raise HTTPException(status_code=404, detail="User with the given code not found. Driver not created.")

        return {"status": "success", "message": "Driver created successfully", "driver_id": user.code}

    async def delete(self, code: int):
        return await self.__driver_repository.delete(code)
