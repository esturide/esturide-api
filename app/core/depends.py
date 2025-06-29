from app.application.uses_cases.auth import AuthUseCase
from app.application.uses_cases.ride import RideCase
from app.application.uses_cases.status import DriverStatusCase, UserStatusCase
from app.application.uses_cases.travel import ScheduleCase
from app.application.uses_cases.user import UserUseCase


def get_auth_case():
    return AuthUseCase()


def get_user_case():
    return UserUseCase()


def get_schedule_case():
    return ScheduleCase()


def get_ride_case():
    return RideCase()


def get_driver_events_case():
    return DriverStatusCase()


def get_passenger_events_case():
    return UserStatusCase()
