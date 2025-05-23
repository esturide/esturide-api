from typing import Annotated, Tuple, Literal

from fastapi import Depends, HTTPException

from app.core.oauth2 import oauth2_scheme, secure_decode
from app.core.types import Token
from app.domain.models import User
from app.infrastructure.repository.user import UserRepository


async def user_credentials(token: Annotated[Token, Depends(oauth2_scheme)]) -> Tuple[Literal[False], None] | Tuple[
    Literal[True], User]:
    if token is None:
        return False, None

    with secure_decode(token) as decoded:
        if code := decoded.get("code"):
            return await UserRepository.get(code=code)
        else:
            return False, None


async def user_is_authenticated(token: Annotated[Token, Depends(oauth2_scheme)]) -> int | None:
    result, user = await user_credentials(token)

    if user is not None:
        return user.code

    raise HTTPException(status_code=401, detail="Not authenticated.")


async def get_user_is_authenticated(token: Annotated[Token, Depends(oauth2_scheme)]) -> User | None:
    result, user = await user_credentials(token)

    if result:
        return user

    raise HTTPException(status_code=401, detail="Not authenticated.")


async def validate_admin_role(token: Annotated[Token, Depends(oauth2_scheme)]) -> bool | None:
    result, user = await user_credentials(token)

    if user is not None:
        return user.is_admin

    raise HTTPException(status_code=401, detail="Not authenticated.")


async def validate_permission_role(token: Annotated[Token, Depends(oauth2_scheme)]) -> bool | None:
    result, user = await user_credentials(token)

    if user is not None:
        return user.is_admin or user.is_staff

    raise HTTPException(status_code=401, detail="Not authenticated.")


async def get_user_credentials_header(headers) -> Tuple[Literal[False], None] | Tuple[Literal[True], User]:
    if access_token := headers.get("access_token"):
        return await user_credentials(access_token)

    if access_token := headers.get("accessToken"):
        return await user_credentials(access_token)

    return False, None
