from fastapi import FastAPI

from app.presentation.api.user_management_system.driver import driver
from app.presentation.api.user_management_system.user import user

user_management_system = FastAPI(title="User Management System (μ) API")

user_management_system.include_router(user)
user_management_system.include_router(driver)
