from app.domain.services.automobile import AutomobileService
from app.presentation.schemes import AutomobileRequest

class AutomobileUseCase:
    def __init__(self):
        self.service = AutomobileService()

    async def get(self, code: int):
        return await self.service.get_automobile_by_code(code)

    async def create(self, automobile_request: AutomobileRequest):
        return await self.service.create_automobile(automobile_request)

    async def update(self, code: int, automobile_request: AutomobileRequest):
        return await self.service.update_automobile(code, automobile_request)

    async def delete(self, code: int):
        return await self.service.delete_automobile(code)