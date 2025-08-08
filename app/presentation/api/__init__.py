from fastapi import APIRouter

from app.core.dependencies import OAuth2Scheme, DependAuthCase, DependSessionCase
from app.core.enum import Status
from app.presentation.schemes import StatusMessage
from app.presentation.schemes.session import SessionResponse, SessionType

root = APIRouter(
    tags=["Root"]
)


@root.get('/', response_model=StatusMessage)
async def index():
    return {
        'status': Status.success,
        'message': "Everything works correctly."
    }


@root.get('/session')
async def backup_user_session(token: OAuth2Scheme, session: DependSessionCase) -> SessionResponse:
    return await session.get_current_user_session(token)
