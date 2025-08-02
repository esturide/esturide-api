import typing
import uuid

from fastapi import UploadFile

UserType = typing.TypeVar("UserType")

DocumentRequest = typing.TypeVar("DocumentRequest", UploadFile, bytes)
UUID = typing.TypeVar("UUID", str, uuid.UUID)
Token = typing.TypeVar("Token", str, bytes)
UserCode = typing.TypeVar("UserCode", bound=int)
