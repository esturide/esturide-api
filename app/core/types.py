import typing
import uuid

from fastapi import UploadFile
from enum import Enum

UserType = typing.TypeVar("UserType")

DocumentRequest = typing.TypeVar("DocumentRequest", UploadFile, bytes)
UUID = typing.TypeVar("UUID", str, uuid.UUID)
Token = typing.TypeVar("Token", str, bytes)


class Status(str, Enum):
    success = 'success'
    failure = 'failure'


class Gender(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'
