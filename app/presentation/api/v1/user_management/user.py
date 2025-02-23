from fastapi import APIRouter

from app.core.dependencies import DependUserUseCase, AdminAuthenticated, UserCodeCredentials
from app.core.types import Status, UserCode
from app.presentation.schemes import UserRequest, ProfileUpdateRequest, StatusMessage, UserResponse

user = APIRouter(
    prefix="/user",
    tags=["User management"],
)


@user.post('/', response_model=StatusMessage)
async def create_user(user: UserRequest, user_case: DependUserUseCase):
    status = await user_case.create(user)

    if status:
        return {
            "status": Status.success,
            "message": "User created successfully."
        }

    return {
        "status": Status.failure,
        "message": "User could not be created."
    }


@user.get('/{code}')
async def get_user(code: UserCode, user_case: DependUserUseCase) -> UserResponse:
    return await user_case.get_by_uuid(code)


@user.put('/{code}', response_model=StatusMessage)
async def update_user(code: UserCode, user: ProfileUpdateRequest, user_case: DependUserUseCase,
                      user_code: UserCodeCredentials):
    status = await user_case.set_status(code, user, user_code)

    if status:
        return {
            "status": Status.success,
            "message": "User profile updated successfully."
        }

    return {
        "status": Status.failure,
        "message": "User profile update failed."
    }


@user.delete('/{code}', response_model=StatusMessage)
async def delete_user(code: UserCode, user_case: DependUserUseCase, user_code: UserCodeCredentials,
                      is_admin: AdminAuthenticated):
    status = await user_case.delete(code, user_code, is_admin)

    if status:
        return {
            "status": Status.success,
            "message": "User is deleted."
        }

    return {
        "status": Status.failure,
        "message": "User is not deleted."
    }
