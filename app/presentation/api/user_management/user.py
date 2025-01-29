from fastapi import APIRouter

from app.core.dependencies import DependUserManagementCase, AdminAuthenticated, AuthUserCredentials, OAuth2Scheme, DependAuthCase
from app.presentation.schemes import UserRequest, ProfileUpdateRequest

user = APIRouter(
    prefix="/user",
    tags=["User management"],
)


@user.post('/')
async def create_user(user: UserRequest, user_case: DependUserManagementCase):
    status = await user_case.create(user)

    return {
        "status": "success" if status else "failure",
    }


@user.get('/{code}')
async def get_user(code: int, user_case: DependUserManagementCase):
    return await user_case.get(code)


@user.put('/{code}')
async def update_user(code: int, user: ProfileUpdateRequest, user_case: DependUserManagementCase,
                      auth_user: AuthUserCredentials):
    status = await user_case.update(code, user, auth_user.code)

    return {
        "status": "success" if status else "failure",
    }


@user.delete('/{code}')
async def delete_user(code: int, user_case: DependUserManagementCase, auth_user: AuthUserCredentials,
                      is_admin: AdminAuthenticated):
    status = await user_case.delete(code, auth_user.code, is_admin)

    return {
        "status": "success" if status else "failure",
    }

@user.post('/check')
async def check_token(token: OAuth2Scheme, auth: DependAuthCase):
    status = await auth.check(token)

    if status:
        return {"status": "success"}
    else:
        return {"status": "failed"}

@user.post('/profile')
async def get_profile(token: OAuth2Scheme, auth: DependAuthCase):
    return await auth.get_user_profile(token)

