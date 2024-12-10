from fastapi import APIRouter

from app.core.dependencies import DependUserManagementCase
from app.presentation.schemes import UserRequest, ProfileUpdateRequest

driver = APIRouter(
    prefix="/driver",
    tags=["Driver and car management"],
)


@driver.post('/')
async def register_automobile(user: UserRequest):
    return {"message" : f"automobile correctly registered"}

@driver.get('/{code}')
async def get_automobile(code: int):
    ...


@driver.put('/{code}')
async def update_automobile(code: int, user: ProfileUpdateRequest):
    ...


@driver.delete('/{code}')
async def delete_automobile(code: int, user_case: DependUserManagementCase):
    ...
