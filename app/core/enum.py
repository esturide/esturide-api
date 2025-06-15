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
