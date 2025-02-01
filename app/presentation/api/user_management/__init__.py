from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, HTTPException

from app.presentation.api.user_management.driver import driver
from app.presentation.api.user_management.user import user
from app.presentation.api.user_management.automobile import automobile_router

user_management_system = FastAPI(title="User Management System (μ) API")

user_management_system.include_router(user)
user_management_system.include_router(driver)
user_management_system.include_router(automobile_router)


@user_management_system.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    raise HTTPException(
        status_code=400,
        detail="User data or driver request was invalid"
    )
