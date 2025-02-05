from fastapi import APIRouter

from app.core.dependencies import DependAutomobileUseCase, AuthUserCredentials
from app.presentation.schemes import AutomobileRequest, AutomobileResponse

automobile_router = APIRouter(
    prefix="/automobile",
    tags=["Automobile Management"],
)


@automobile_router.get("/{code}", response_model=AutomobileResponse)
async def get_automobile(code: int, auto_case: DependAutomobileUseCase, auth_user: AuthUserCredentials):
    return await auto_case.get(code)


@automobile_router.post("/", response_model=AutomobileResponse)
async def create_automobile(automobile_request: AutomobileRequest,
                            auto_case: DependAutomobileUseCase, auth_user: AuthUserCredentials):
    return await auto_case.create(automobile_request)


@automobile_router.put("/{code}", response_model=AutomobileResponse)
async def update_automobile(code: int, automobile_request: AutomobileRequest,
                            auto_case: DependAutomobileUseCase, auth_user: AuthUserCredentials):
    return await auto_case.update(code, automobile_request)


@automobile_router.delete("/{code}")
async def delete_automobile(code: int, auto_case: DependAutomobileUseCase, auth_user: AuthUserCredentials):
    return await auto_case.delete(code)
