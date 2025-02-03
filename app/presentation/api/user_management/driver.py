from fastapi import APIRouter

from app.core.dependencies import DependDriverUseCase, AdminAuthenticated, AuthUserCredentials
from app.core.types import UserCode, Status
from app.presentation.schemes import UserRequest, StatusMessage

driver = APIRouter(
    prefix="/driver",
    tags=["Driver management"],
)

@driver.post('/', response_model=StatusMessage)
async def create_driver(driver_request: UserRequest, driver_case: DependDriverUseCase):
    response = await driver_case.create(driver_request)
    return response


@driver.patch('/{code}', response_model=StatusMessage)
async def set_driver(code: UserCode, driver_case: DependDriverUseCase, auth: AuthUserCredentials, is_admin: AdminAuthenticated):
    status = await driver_case.set_user_driver(code)

    if status:
        return {
            "status": Status.success,
            "message": f"User Profile {code} has been updated, he is now a driver"
        }

    return {
        "status": Status.failure,
        "message": "Cannot change user profile."
    }


@driver.delete('/{code}', response_model=StatusMessage)
async def delete_driver(code: UserCode, uuid_user_code: int, driver_case: DependDriverUseCase, is_admin: AdminAuthenticated):
    status = await driver_case.delete(code, uuid_user_code)

    if status:
        return {
            "status": Status.success,
            "message": "Driver deleted successfully."
        }

    return {
        "status": Status.failure,
        "message": "Driver could not be deleted."
    }
