from datetime import datetime, date

from app.domain.models import User


def convert_date(_date: date) -> datetime:
    return datetime.combine(_date.today(), datetime.min.time())


class UserRepository:
    @staticmethod
    async def get(**kwargs) -> tuple[False, None] | tuple[True, User]:
        user = await User.nodes.get_or_none(**kwargs)

        if user is None:
            return False, None

        return True, user

    @staticmethod
    async def get_user_by_code(code: int):
        return await UserRepository.get(code=code)

    @staticmethod
    async def get_user_by_email(email: str):
        return await UserRepository.get(email=email)

    @staticmethod
    async def create(
            code: int,
            firstname: str,
            maternal_surname: str,
            paternal_surname: str,
            curp: str,
            birth_date: datetime.date,
            email: str,
            password: str,
    ):
        user = User(
            code=code,
            firstname=firstname,
            maternal_surname=maternal_surname,
            paternal_surname=paternal_surname,
            curp=curp,
            birth_date=convert_date(birth_date),
            email=email,
            password=password,
        )

        status, _ = await UserRepository.get_user_by_code(code)

        if status:
            return False, None

        await user.save()

        return True, user

    @staticmethod
    async def update(
            code: int,
            firstname: str,
            maternal_surname: str,
            paternal_surname: str,
            curp: str,
            birth_date: datetime.date,
            email: str,
            password: str,
    ):
        status, user = await UserRepository.get_user_by_code(code)

        user.firstname = firstname
        user.maternal_surname = maternal_surname
        user.paternal_surname = paternal_surname
        user.curp = curp
        user.birth_date = convert_date(birth_date)
        user.email = email
        user.password = password

        await user.save()

        return True, user

    @staticmethod
    async def delete(code: int) -> bool:
        status, user = await UserRepository.get(code=code)

        if not status:
            return False

        await user.delete()

        return True
