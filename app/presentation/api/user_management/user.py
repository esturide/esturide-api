from fastapi import APIRouter

from app.core.dependencies import DependUserUseCase, AdminAuthenticated, AuthUserCredentials, OAuth2Scheme, \
    DependAuthCase
from app.core.types import Status
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
async def get_user(code: int, user_case: DependUserUseCase) -> UserResponse:
    return await user_case.get(code)


@user.put('/{code}', response_model=StatusMessage)
async def update_user(code: int, user: ProfileUpdateRequest, user_case: DependUserUseCase,
                      auth_user: AuthUserCredentials):
    status = await user_case.update(code, user, auth_user.code)

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
async def delete_user(code: int, user_case: DependUserUseCase, auth_user: AuthUserCredentials,
                      is_admin: AdminAuthenticated):
    status = await user_case.delete(code, auth_user.code, is_admin)

    if status:
        return {
            "status": Status.success,
            "message": "User is deleted."
        }

    return {
        "status": Status.failure,
        "message": "User is not deleted."
    }


@user.post('/check', response_model=StatusMessage)
async def check_token(token: OAuth2Scheme, auth: DependAuthCase):
    status = await auth.check(token)

    if status:
        return {
            "status": Status.success,
            "message": "Validate token."
        }

    return {
        "status": Status.failure,
        "message": "Invalid token."
    }


@user.post('/profile')
async def get_profile(token: OAuth2Scheme, auth: DependAuthCase) -> UserResponse:
    return await auth.get_user_profile(token)
