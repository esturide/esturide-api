from fastapi import APIRouter
from passlib.context import CryptContext

from app.core.dependencies import OAuth2Form, DependAuthCase, OAuth2Scheme
from app.core.types import Status
from app.presentation.schemes import StatusMessage, StatusResponse
from app.presentation.schemes.auth import AccessCredentialForm, AccessCredential, AccessLogin

auth = APIRouter(
    prefix="/auth",
    tags=["Auth router"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@auth.post("/", response_model=AccessCredentialForm)
async def login_from_form(form: OAuth2Form, auth: DependAuthCase):
    code = form.username
    password = form.password

    token = await auth.login(code, password)

    return {
        "access_token": token,
    }


@auth.post("/login", response_model=AccessCredential)
async def login(access: AccessLogin, auth: DependAuthCase):
    token = await auth.login(access.username, access.password.get_secret_value())

    return {
        "token": token,
    }


@auth.post("/logout", response_model=StatusMessage)
async def logout(token: OAuth2Scheme, auth: DependAuthCase):
    status = await auth.logout(token)

    if status:
        return {
            "status": Status.success,
            "message": "Loggout successful."
        }

    return {
        "status": Status.failure,
        "message": "Loggout failed."
    }


@auth.post("/check", response_model=StatusMessage)
async def check_token(token: OAuth2Scheme, auth: DependAuthCase):
    status = await auth.check(token)

    if status:
        return {
            "status": Status.success,
            "message": "Validate token."
        }

    return {
        "status": Status.failure,
        "message": "Invalid token."
    }


@auth.post("/refresh", response_model=StatusResponse[AccessCredential])
async def refresh_token(token: OAuth2Scheme, auth: DependAuthCase):
    token = await auth.refresh(token)

    return {
        "status": Status.success,
        "data": AccessCredential(
            token=token,
        )
    }
