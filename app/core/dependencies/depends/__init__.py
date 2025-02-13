from functools import lru_cache

from app.application.uses_cases.auth import AuthUseCase
from app.application.uses_cases.automobile import AutomobileUseCase
from app.application.uses_cases.driver import DriverUseCase
from app.application.uses_cases.ride import RideCase
from app.application.uses_cases.status import DriverStatusCase, UserStatusCase, EventsTestingCase
from app.application.uses_cases.status.socket import EventsSocket
from app.application.uses_cases.status.socket.driver import DriverEventsSocket
from app.application.uses_cases.status.socket.passenger import PassengerEventsSocket
from app.application.uses_cases.travel import ScheduleCase
from app.application.uses_cases.user import UserUseCase
from app.core.manager.sockets import SocketConnectionManager


@lru_cache
def get_auth_case():
    return AuthUseCase()


@lru_cache
def get_user_case():
    return UserUseCase()


@lru_cache
def get_schedule_case():
    return ScheduleCase()


@lru_cache
def get_ride_case():
    return RideCase()


@lru_cache
def get_driver_events_case():
    return DriverStatusCase()


@lru_cache
def get_passenger_events_case():
    return UserStatusCase()


@lru_cache
def get_events_testing_case():
    return EventsTestingCase()


@lru_cache
def get_events_socket():
    return EventsSocket()


@lru_cache
def get_driver_events_socket():
    return DriverEventsSocket()


@lru_cache
def get_passenger_events_socket():
    return PassengerEventsSocket()


@lru_cache
def get_socket_connection_manager():
    return SocketConnectionManager()


@lru_cache
def get_automobile_use_case() -> AutomobileUseCase:
    return AutomobileUseCase()


@lru_cache
def get_driver_case() -> DriverUseCase:
    return DriverUseCase()
