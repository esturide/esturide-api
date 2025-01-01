from app.infrastructure.repository.automobile import AutomobileRepository
from app.presentation.schemes import AutomobileRequest, AutomobileResponse
from fastapi import HTTPException

class AutomobileService:
    def __init__(self):
        self.repository = AutomobileRepository()

    async def get_automobile_by_code(self, code: int):
        automobile = await self.repository.get_automobile_by_code(code)
        if not automobile:
            raise HTTPException(status_code=404, detail="Automobile not found")
        return automobile

    async def create_automobile(self, automobile_request: AutomobileRequest):
        existing_car = await self.repository.get_automobile_by_code(automobile_request.code)
        if existing_car:
            raise HTTPException(status_code=400, detail="Automobile with this code already exists")

        automobile = await self.repository.create_automobile(
            code=automobile_request.code,
            brand=automobile_request.brand,
            year=automobile_request.year,
            model=automobile_request.model,
        )
        return AutomobileResponse(
            code=automobile.code,
            brand=automobile.brand,
            year=automobile.year,
            model=automobile.model,
        )

    async def update_automobile(self, code: int, automobile_request: AutomobileRequest):
        automobile = await self.repository.get_automobile_by_code(code)
        if not automobile:
            raise HTTPException(status_code=404, detail="Automobile not found")

        updated_automobile = await self.repository.update_automobile(
            automobile,
            brand=automobile_request.brand,
            year=automobile_request.year,
            model=automobile_request.model,
        )
        return AutomobileResponse(
            code=updated_automobile.code,
            brand=updated_automobile.brand,
            year=updated_automobile.year,
            model=updated_automobile.model,
        )

    async def delete_automobile(self, code: int):
        automobile = await self.repository.get_automobile_by_code(code)
        if not automobile:
            raise HTTPException(status_code=404, detail="Automobile not found")

        await self.repository.delete_automobile(automobile)
        return {"status": "success", "message": "Automobile deleted successfully"}
