from app.core.dataclass import DataDriverCurrentSession, DataPassengerCurrentSession
from app.core.enum import CurrentRuleUser
from app.core.types import Token
from app.domain.services.auth import AuthenticationCredentialsService
from app.domain.services.user import UserService
from app.presentation.schemes.session import SessionResponse


class SessionUseCase:
    def __init__(self):
        self.__user_service = UserService()
        self.__auth_service = AuthenticationCredentialsService()

    async def get_current_user_session(self, token: Token) -> SessionResponse:
        user = await self.__user_service.get_by_token(token)
        session = user.last_session

        if isinstance(session, DataDriverCurrentSession):
            return SessionResponse(
                code=user.code,
                currentRole=CurrentRuleUser.driver,
                current={
                    "schedule": session.schedule,
                    "driverTo": session.driver_to,
                }
            )
        elif isinstance(session, DataPassengerCurrentSession):
            return SessionResponse(
                code=user.code,
                currentRole=CurrentRuleUser.passenger,
                current={
                    "schedule": session.schedule,
                    "rideTo": session.ride_to,
                }
            )
        else:
            return SessionResponse(
                code=user.code,
                currentRole=CurrentRuleUser.no_session,
            )
