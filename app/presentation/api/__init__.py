from fastapi import APIRouter

from app.core.enum import Status
from app.presentation.schemes import StatusMessage

root = APIRouter(
    tags=["Root"]
)


@root.get('/', response_model=StatusMessage)
async def index():
    return {
        'status': Status.success,
        'message': "Everything works correctly."
    }
