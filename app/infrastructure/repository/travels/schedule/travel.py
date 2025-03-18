from neomodel import DoesNotExist

from app.core.exception import NotFoundException
from app.domain.models import Schedule, User, Travel


class TravelRepository:
    @staticmethod
    async def get(schedule: Schedule, driver: User) -> Travel:
        try:
            travel = await driver.schedules.relationship(schedule)

            if travel is None:
                raise NotFoundException("Travel not found.")

        except DoesNotExist:
            raise NotFoundException("Travel not found.")
        else:
            return travel
