from fastapi import APIRouter

from app.core.dependencies import DependUserManagementCase
from app.domain.factory.users import create_dummy_user_data
from app.presentation.schemes import UserRequest

factory = APIRouter(
    tags=["Factories"]
)


@factory.post('/user')
async def factory_user(user_case: DependUserManagementCase, limit: int = 30):
    status = True

    for _ in range(limit):
        data = create_dummy_user_data()

        await user_case.create(
            UserRequest(**data),
        )

    return {
        "status": "success" if status else "failure",
    }
