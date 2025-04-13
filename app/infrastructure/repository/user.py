import contextlib
from datetime import date
from typing import Literal

from app.core.encrypt import salty_password
from app.core.exception import NotFoundException
from app.core.oauth2 import get_code_from_token
from app.core.types import Token, UserCode
from app.domain.models import User


class UserRepository:
    @staticmethod
    async def get(**kwargs) -> tuple[Literal[False], None] | tuple[Literal[True], User]:
        user = await User.nodes.get_or_none(**kwargs)

        return user is not None, user

    @staticmethod
    async def get_user_by_code(code: UserCode):
        return await UserRepository.get(code=code)

    @staticmethod
    async def get_user_by_email(email: str):
        return await UserRepository.get(email=email)

    @staticmethod
    async def get_user_by_token(token: Token):
        return await UserRepository.get_user_by_code(
            get_code_from_token(token)
        )

    @staticmethod
    async def user_exist_by_email(email: str):
        result, user = await UserRepository.get_user_by_email(email)

        return result

    @staticmethod
    async def user_exist_by_username(code: UserCode):
        result, user = await UserRepository.get_user_by_code(code)

        return result

    @staticmethod
    async def create(
            code: UserCode,
            firstname: str,
            maternal_surname: str,
            paternal_surname: str,
            curp: str,
            birth_date: date,
            email: str,
            password: str,
    ):
        salt, hashed_password = salty_password(password)

        if await UserRepository.user_exist_by_email(email) or await UserRepository.user_exist_by_username(code):
            return False, None

        user = User(
            code=code,
            hashed_password=hashed_password,
            salt=salt,

            firstname=firstname,
            maternal_surname=maternal_surname,
            paternal_surname=paternal_surname,
            birth_date=birth_date,

            email=email,
            curp=curp,
        )

        await user.save()

        return True, user

    @staticmethod
    async def update(
            code: UserCode,
            firstname: str,
            maternal_surname: str,
            paternal_surname: str,
            curp: str,
            birth_date: date,
            email: str,
            password: str,
    ):
        status, user = await UserRepository.get_user_by_code(code)

        if not user.same_password(password):
            salt, hashed_password = salty_password(password)

            user.hashed_password = hashed_password
            user.salt = salt

        user.firstname = firstname
        user.maternal_surname = maternal_surname
        user.paternal_surname = paternal_surname
        user.curp = curp
        user.birth_date = birth_date
        user.email = email
        user.password = password

        await user.save()

        return True, user

    @staticmethod
    async def save(user: User) -> bool:
        await user.save()

        return True

    @staticmethod
    async def delete(code: UserCode) -> bool:
        status, user = await UserRepository.get(code=code)

        if not status:
            return False

        await user.delete()

        return True


class UserRepositoryContext:
    @contextlib.asynccontextmanager
    async def create(self,
                     code: UserCode,
                     firstname: str,
                     maternal_surname: str,
                     paternal_surname: str,
                     curp: str,
                     birth_date: date,
                     email: str,
                     password: str,
                     exception=False):
        user, result = await UserRepository.create(
            code,
            firstname,
            maternal_surname,
            paternal_surname,
            curp,
            birth_date,
            email,
            password
        )

        if user is not None:
            yield user
        else:
            if exception:
                raise NotFoundException(detail="User not created.")

        return

    @contextlib.asynccontextmanager
    async def get(self, exception=False, **kwargs):
        user, result = await UserRepository.get(**kwargs)

        if user is not None:
            yield user
        else:
            if exception:
                raise NotFoundException(detail="User not found.")

        return

    @contextlib.asynccontextmanager
    async def patch(self, exception=False, **kwargs):
        user, result = await UserRepository.get(**kwargs)

        if user is not None:
            yield user
            await user.save()
        else:
            if exception:
                raise NotFoundException(detail="User not patch.")

        return
