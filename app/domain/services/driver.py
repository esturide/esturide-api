from fastapi import HTTPException

from app.core import settings
from app.core.oauth2 import encode, check_if_expired, secure_decode
from app.core.types import Token
from app.infrastructure.repository.user import Driver
from app.presentation.schemes import UserRequest, ProfileUpdateRequest

class DriverService : 
    def __init__(self):
        self.__