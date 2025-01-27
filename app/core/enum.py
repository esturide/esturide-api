from enum import Enum


class Status(str, Enum):
    success = 'success'
    failure = 'failure'
