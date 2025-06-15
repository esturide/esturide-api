from app.core.exception import NotFoundException
from app.core.types import UserCode
from app.domain.models import Schedule, Travel
from app.infrastructure.repository.travels.schedule.travel import TravelRepository
from app.infrastructure.repository.user import UserRepository


class TravelService:
    async def get(self, schedule: Schedule, code: UserCode) -> Travel:
        _, user = await UserRepository.get_user_by_code(code)

        if user is None:
            raise NotFoundException("Driver not found.")

        return await TravelRepository.get(schedule, user)
