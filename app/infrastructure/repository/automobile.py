from app.domain.models import Automobile

class AutomobileRepository:
    @staticmethod
    async def get_automobile_by_code(code: int):
        """
        Busca un automóvil por su código único.
        """
        return await Automobile.nodes.get_or_none(code=code)

    @staticmethod
    async def create_automobile(code: int, brand: str, year: int, model: str):
        """
        Crea un nuevo automóvil.
        """
        automobile = Automobile(code=code, brand=brand, year=year, model=model)
        await automobile.save()
        return automobile

    @staticmethod
    async def update_automobile(automobile: Automobile, brand: str, year: int, model: str):
        automobile.brand = brand
        automobile.year = year
        automobile.model = model
        await automobile.save()
        return automobile

    @staticmethod
    async def delete_automobile(automobile: Automobile):
        await automobile.delete()
        return True
