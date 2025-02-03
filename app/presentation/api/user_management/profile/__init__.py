from fastapi import APIRouter

from app.core.dependencies import OAuth2Scheme, DependAuthCase, DependUserUseCase
from app.core.enum import RoleUser
from app.core.types import Status
from app.presentation.schemes import UserResponse, StatusResponse

profile = APIRouter(
    prefix="/profile",
    tags=["User profile"],
)


@profile.get('/', response_model=UserResponse)
async def get_profile(token: OAuth2Scheme, auth: DependAuthCase):
    return await auth.get_user_profile(token)


@profile.get('/role', response_model=StatusResponse[RoleUser])
async def get_role(token: OAuth2Scheme, user_case: DependUserUseCase):
    role = await user_case.get_user_role(token)

    return {
        "status": Status.success,
        "data": role
    }
