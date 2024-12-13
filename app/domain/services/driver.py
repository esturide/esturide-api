from app.infrastructure.repository.driver import DriverRepository
from app.presentation.schemes import UserRequest, ProfileUpdateRequest


class DriverService:
    def __init__(self):
        self.__driver_repository = DriverRepository()

    async def get_by_code(self, driver_code: int):
        return await self.__driver_repository.get_driver_by_code(driver_code)

    async def create(self, user_req: UserRequest):
        return await self.__driver_repository.create(
            code=user_req.code,
            firstname=user_req.firstname,
            maternal_surname=user_req.maternal_surname,
            paternal_surname=user_req.paternal_surname,
            curp=user_req.curp,
            birth_date=user_req.birth_date,
            email=user_req.email,
            password=user_req.password,
        )

    async def update(self, code: int, driver_req: ProfileUpdateRequest):
        status, driver = await self.__driver_repository.get_driver_by_code(code)

        if not status:
            return False, None

        return await self.__driver_repository.create(
            code=code,
            firstname=driver_req.firstname,
            maternal_surname=driver_req.maternal_surname,
            paternal_surname=driver_req.paternal_surname,
            curp=driver_req.curp,
            birth_date=driver_req.birth_date,
            email=driver_req.email,
            password=driver_req.password,
        )

    async def delete(self, code: int):
        return await self.__driver_repository.delete(code)
