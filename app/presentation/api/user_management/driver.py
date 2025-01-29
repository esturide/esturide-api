from fastapi import APIRouter, Depends
from app.core.dependencies import DependUserManagementCase, AdminAuthenticated, AuthUserCredentials
from app.presentation.schemes import UserRequest, ProfileUpdateRequest
from app.application.uses_cases.driver import DriverUseCase

driver = APIRouter(
    prefix="/driver",
    tags=["Driver management"],
)

def get_driver_case() -> DriverUseCase:
    return DriverUseCase()


@driver.post('/')
async def create_driver(driver_request: UserRequest, driver_case: DriverUseCase = Depends(get_driver_case)):
    response = await driver_case.create(driver_request)
    return response

@driver.get('/{code}')
async def get_driver(code: int, driver_case: DriverUseCase = Depends(get_driver_case)):
    return await driver_case.get(code)

@driver.delete('/{code}')
async def delete_driver(code: int, uuid_user_code: int, driver_case: DriverUseCase = Depends(get_driver_case)):
    status = await driver_case.delete(code, uuid_user_code)
    return {"status": "success" if status else "failure"}
