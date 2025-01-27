from typing import Annotated, Tuple, Optional

from fastapi import Depends, File
from fastapi.security import OAuth2PasswordRequestForm
from neomodel.sync_.core import Database

from app.application.uses_cases.auth import AuthUseCase
from app.application.uses_cases.ride import RideCase
from app.application.uses_cases.status import DriverStatusCase, UserStatusCase, EventsTestingCase
from app.application.uses_cases.status.socket import EventsSocket, DriverEventsSocket, PassengerEventsSocket
from app.application.uses_cases.travel import ScheduleCase
from app.application.uses_cases.user import UserUseCase
from app.core import connect_db
from app.core.depends import get_user_case, get_auth_case, get_schedule_case, get_ride_case, get_driver_events_case, \
    get_passenger_events_case, get_events_testing_case, get_events_socket, get_driver_events_socket, \
    get_passenger_events_socket
from app.core.oauth2 import oauth2_scheme
from app.core.types import Token
from app.domain.credentials import user_credentials, validate_admin_role, \
    validate_permission_role, get_user_is_authenticated
from app.domain.models import User

DependUserManagementCase = Annotated[UserUseCase, Depends(get_user_case)]
DependAuthCase = Annotated[AuthUseCase, Depends(get_auth_case)]
DependScheduleCase = Annotated[ScheduleCase, Depends(get_schedule_case)]
DependRideCase = Annotated[RideCase, Depends(get_ride_case)]
DependDriverEventsCase = Annotated[DriverStatusCase, Depends(get_driver_events_case)]
DependPassengerEventsCase = Annotated[UserStatusCase, Depends(get_passenger_events_case)]
DependEventsTestingCase = Annotated[EventsTestingCase, Depends(get_events_testing_case)]
DependEventsSocketCase = Annotated[EventsSocket, Depends(get_events_socket)]
DependDriverEventsSocketCase = Annotated[DriverEventsSocket, Depends(get_driver_events_socket)]
DependPassengerEventsSocketCase = Annotated[PassengerEventsSocket, Depends(get_passenger_events_socket)]

OAuth2Scheme = Annotated[Token, Depends(oauth2_scheme)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
UserCredentials = Annotated[Tuple[bool, Optional[User]], Depends(user_credentials)]
AuthUserCredentials = Annotated[User, Depends(get_user_is_authenticated)]
AdminAuthenticated = Annotated[bool, Depends(validate_admin_role)]
ManagerAuthenticated = Annotated[bool, Depends(validate_permission_role)]

DataBaseDepend = Annotated[Database, Depends(connect_db)]

FileRequest = Annotated[bytes | None, File()]
