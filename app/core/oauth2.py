import contextlib
from datetime import timedelta, datetime

import jwt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core import settings
from app.core.types import Token


def create_oauth2_token(url="/auth/"):
    _oauth2_scheme = OAuth2PasswordBearer(url)

    def get_oauth2():
        return _oauth2_scheme

    return get_oauth2


get_oauth2_token = create_oauth2_token()


def encode(data: dict, expires_minutes: int) -> Token:
    data_to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=expires_minutes)

    data_to_encode.update({
        "exp": expire
    })

    return jwt.encode(data_to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode(token: Token) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])


def check_if_expired(token: Token) -> bool:
    try:
        decode(token)
    except jwt.ExpiredSignatureError:
        return False
    finally:
        return True


@contextlib.contextmanager
def secure_decode(token: Token):
    try:
        yield decode(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
        )


oauth2_scheme = get_oauth2_token()
