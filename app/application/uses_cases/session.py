from fastapi import HTTPException

from app.core.enum import RoleUser
from app.core.types import Token, UserCode
from app.domain.services.auth import AuthenticationCredentialsService
from app.domain.services.user import UserService
from app.infrastructure.repository.user import UserRepository
from app.presentation.schemes import UserRequest, UserResponse, ProfileUpdateRequest
from app.presentation.schemes.session import SessionResponse


class SessionUseCase:
    def __init__(self):
        self.__user_service = UserService()
        self.__auth_service = AuthenticationCredentialsService()

    async def get_current_user_session(self, token: Token) -> SessionResponse:
        user = await self.__user_service.get_by_token(token)

        return SessionResponse(

        )
