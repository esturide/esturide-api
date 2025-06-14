from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, HTTPException

from app.presentation.api.v1.user_management.automobile import automobile_router
from app.presentation.api.v1.user_management.driver import driver
from app.presentation.api.v1.user_management.profile import profile
from app.presentation.api.v1.user_management.user import user
from app.presentation.api.v1.user_management.tracking import tracking

user_management_v1 = FastAPI(title="User Management (μ) API")

user_management_v1.include_router(profile)
user_management_v1.include_router(user)
user_management_v1.include_router(driver)
user_management_v1.include_router(automobile_router)
user_management_v1.include_router(tracking)


@user_management_v1.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    raise HTTPException(
        status_code=400,
        detail="User data or driver request was invalid."
    )
