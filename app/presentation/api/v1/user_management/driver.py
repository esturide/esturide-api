from fastapi import APIRouter

from app.core.dependencies import DependDriverUseCase, AdminAuthenticated, AuthUserCredentials, OAuth2Scheme
from app.core.types import UserCode, Status
from app.presentation.schemes import StatusMessage

driver = APIRouter(
    prefix="/driver",
    tags=["Driver management"],
)


@driver.patch('/', response_model=StatusMessage)
async def set_user_driver(token: OAuth2Scheme, driver_case: DependDriverUseCase):
    status = await driver_case.set_user_driver(token)

    if status:
        return {
            "status": Status.success,
            "message": f"User Profile has been updated, he is now a driver."
        }

    return {
        "status": Status.failure,
        "message": "Cannot change user profile."
    }


@driver.get('/{code}', response_model=StatusMessage)
async def validate_driver(code: UserCode, driver_case: DependDriverUseCase):
    status = await driver_case.check_user_driver(code)

    if status:
        return {
            "status": Status.success,
            "message": "User is valid to drive."
        }

    return {
        "status": Status.failure,
        "message": "User is not valid to drive."
    }
