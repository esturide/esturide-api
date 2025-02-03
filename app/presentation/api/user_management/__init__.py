from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, HTTPException

from app.presentation.api.user_management.automobile import automobile_router
from app.presentation.api.user_management.driver import driver
from app.presentation.api.user_management.profile import profile
from app.presentation.api.user_management.user import user

user_management = FastAPI(title="User Management (μ) API")

user_management.include_router(profile)
user_management.include_router(user)
user_management.include_router(driver)
user_management.include_router(automobile_router)


@user_management.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    raise HTTPException(
        status_code=400,
        detail="User data or driver request was invalid."
    )
