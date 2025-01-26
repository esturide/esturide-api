
from fastapi import APIRouter, HTTPException

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


@root.get('/error', response_model=StatusMessage)
async def index():
    raise HTTPException(
        status_code=400,
        detail="Error message"
    )
