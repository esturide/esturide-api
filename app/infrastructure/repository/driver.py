from datetime import date
from typing import Literal

from app.domain.models import User


class DriverRepository:
    @staticmethod
    async def get(**kwargs) -> tuple[Literal[False], None] | tuple[Literal[True], User]:
        kwargs['role'] = 'D'
        user = await User.nodes.get_or_none(**kwargs)
        if user is None:
            return False, None

        return True, user

    @staticmethod
    async def get_driver_by_code(code: int):
        return await DriverRepository.get(code=code)

    @staticmethod
    async def create_or_update(
            code: int,
            firstname: str,
            maternal_surname: str,
            paternal_surname: str,
            curp: str,
            birth_date: date,
            email: str,
            password: str,
    ):
        user = await User.nodes.get_or_none(code=code)

        if user is None:
            return False, None

        user.firstname = firstname
        user.maternal_surname = maternal_surname
        user.paternal_surname = paternal_surname
        user.curp = curp
        user.birth_date = birth_date
        user.email = email
        user.password = password
        user.role = 'D'

        await user.save()

        return True, user

    @staticmethod
    async def delete(code: int) -> bool:
        status, user = await DriverRepository.get_driver_by_code(code)

        if not status:
            return False

        user.valid_user = False
        user.role = 'S'
        await user.save()

        return True
