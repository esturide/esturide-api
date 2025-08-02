from enum import Enum


class Status(str, Enum):
    success = 'success'
    failure = 'failure'


class RoleUser(str, Enum):
    not_verified = 'not-verified'
    driver = 'driver'
    passenger = 'passenger'
    staff = 'staff'
    admin = 'admin'


class CurrentRuleUser(str, Enum):
    no_session = 'no-session'
    driver = 'driver'
    passenger = 'passenger'


class Gender(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'


class StatusTravel(str, Enum):
    start = 'start'
    terminate = 'terminate'
    cancel = 'cancel'