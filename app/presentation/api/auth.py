from fastapi import APIRouter
from passlib.context import CryptContext

from app.core.dependencies import OAuth2Form, DependAuthCase, OAuth2Scheme
from app.presentation.schemes import AccessCredential

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


@auth.post("/check")
async def check_token(token: OAuth2Scheme, auth: DependAuthCase):
    return {
        "status": await auth.check(token),
    }
