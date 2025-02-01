from fastapi import APIRouter

from app.core.dependencies import DependUserManagementCase, AdminAuthenticated, AuthUserCredentials, OAuth2Scheme, DependAuthCase
from app.core.types import Status
from app.presentation.schemes import UserRequest, ProfileUpdateRequest, StatusMessage, UserResponse

user = APIRouter(
    prefix="/user",
    tags=["User management"],
)


@user.post('/', response_model=StatusMessage)
async def create_user(user: UserRequest, user_case: DependUserManagementCase):
    status = await user_case.create(user)

    if status:
        return {
            "status": Status.success,
            "message": "Validate token."
        }

    return {
        "status": Status.failure,
        "message": "Invalid token."
    }


@user.get('/{code}')
async def get_user(code: int, user_case: DependUserManagementCase) -> UserResponse:
    return await user_case.get(code)


@user.put('/{code}', response_model=StatusMessage)
async def update_user(code: int, user: ProfileUpdateRequest, user_case: DependUserManagementCase,
                      auth_user: AuthUserCredentials):
    status = await user_case.update(code, user, auth_user.code)

    if status:
        return {
            "status": Status.success,
            "message": "Validate token."
        }

    return {
        "status": Status.failure,
        "message": "Invalid token."
    }


@user.delete('/{code}', response_model=StatusMessage)
async def delete_user(code: int, user_case: DependUserManagementCase, auth_user: AuthUserCredentials,
                      is_admin: AdminAuthenticated):
    status = await user_case.delete(code, auth_user.code, is_admin)

    if status:
        return {
            "status": Status.success,
            "message": "Validate token."
        }

    return {
        "status": Status.failure,
        "message": "Invalid token."
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

