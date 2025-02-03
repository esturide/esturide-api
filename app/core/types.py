import typing
import uuid
from enum import Enum

from fastapi import UploadFile

UserType = typing.TypeVar("UserType")
M = typing.TypeVar('M')

DocumentRequest = typing.TypeVar("DocumentRequest", UploadFile, bytes)
UUID = typing.TypeVar("UUID", str, uuid.UUID)
Token = typing.TypeVar("Token", str, bytes)
UserCode = typing.TypeVar("UserCode", bound=int)

StatusQuery = typing.Tuple[bool, typing.LiteralString]


class Status(str, Enum):
    success = 'success'
    failure = 'failure'


class Gender(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'
