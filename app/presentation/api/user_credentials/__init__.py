from fastapi import FastAPI

from app.core.types import Status
from app.presentation.schemes import StatusMessage

user_credentials = FastAPI(title="User Credentials (μ) API")


@user_credentials.get("/", response_model=StatusMessage)
async def index():
    return {
        'status': Status.success,
        'message': "Everything works correctly."
    }
