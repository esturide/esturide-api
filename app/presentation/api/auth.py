from fastapi import APIRouter
from passlib.context import CryptContext

from app.core.dependencies import OAuth2Form, DependAuthCase, OAuth2Scheme
from app.core.types import Status
from app.presentation.schemes import AccessCredential, StatusMessage

auth = APIRouter(
    prefix="/auth",
    tags=["Auth router"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@auth.post("/")
async def login(form: OAuth2Form, auth: DependAuthCase) -> AccessCredential:
    code = form.username
    password = form.password

    token = await auth.login(code, password)

    return AccessCredential(
        access_token=token,
    )


@auth.get("/logout")
async def logout(token: OAuth2Scheme, auth: DependAuthCase):
    return await auth.logout(token)


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
