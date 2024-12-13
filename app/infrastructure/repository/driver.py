from datetime import date
from typing import Literal

from app.domain.models import User

class DriverRepository:
    @staticmethod
    async def get(**kwargs) -> tuple[Literal[False] , None ] | tuple[Literal[True], User] :
        kwargs['role'] = 'D'
        user = await User.nodes.get_or_none(**kwargs)
        if user is None : 
            return False , None
        
        return True , user
    
    @staticmethod
    async def get_driver_by_code(code: int):
        return await DriverRepository.get(code=code)
    
    @staticmethod
    async def create(
            code: int,
            firstname: str,
            maternal_surname: str,
            paternal_surname: str,
            curp: str,
            birth_date: date,
            email: str,
            password: str,
    ):
        driver = User(
            code=code,
            firstname=firstname,
            maternal_surname=maternal_surname,
            paternal_surname=paternal_surname,
            curp=curp,
            birth_date=birth_date,
            email=email,
            password=password,
            role='D',  
        )
        status, _ = await DriverRepository.get_driver_by_code(code)

        if status:
            return False, None

        await driver.save()
        
        return True, driver
    
    @staticmethod
    async def delete(code: int) -> bool:
        status, user = await DriverRepository.get_driver_by_code(code)

        if not status:
            return False

        user.valid_user = False
        user.role = 'S'
        await user.save()

        return True
