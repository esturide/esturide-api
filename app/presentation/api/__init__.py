from fastapi import APIRouter

from app.core.dependencies import OAuth2Scheme, DependAuthCase, DependSessionCase
from app.core.enum import Status
from app.presentation.schemes import StatusMessage
from app.presentation.schemes.session import SessionResponse

root = APIRouter(
    tags=["Root"]
)


@root.get('/', response_model=StatusMessage)
async def index():
    return {
        'status': Status.success,
        'message': "Everything works correctly."
    }


@root.get('/session', response_model=SessionResponse)
async def backup_session(token: OAuth2Scheme, session: DependSessionCase):

    return {

    }
