from fastapi import APIRouter

from app.core.dependencies import DependUserManagementCase
from app.domain.factory.users import create_dummy_user_data
from app.presentation.schemes import UserRequest

root = APIRouter(
    tags=["Root"]
)


@root.get('/')
async def index():
    return {
        "msg": "Hello World"
    }


@root.get('/factory/user')
async def factory_user(user_case: DependUserManagementCase):
    status = True

    for _ in range(30):
        data = create_dummy_user_data()

        print(data)

        await user_case.create(
            UserRequest(**data),
        )

    return {
        "status": "success" if status else "failure",
    }

