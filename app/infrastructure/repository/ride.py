import dataclasses
from typing import Tuple, Literal

from app.domain.models import Schedule, User, Ride


@dataclasses.dataclass
class RideData:
    location: str
    latitude: str
    longitude: str


class RideRepository:
    @staticmethod
    async def get(schedule: Schedule, passenger: User) -> Tuple[Literal[False], None] | Tuple[Literal[True], Ride]:
        try:
            ride = await passenger.rides.relationship(schedule)

            if ride is None:
                return False, None

        except Ride.DoesNotExist:
            return False, None
        else:
            return True, ride

    @staticmethod
    async def get_all(schedule: Schedule):
        passengers = await schedule.passengers.all()

        rides = []

        for passenger in passengers:
            _, ride = await RideRepository.get(schedule, passenger)
            rides.append(ride)

        return rides

    @staticmethod
    async def create(schedule: Schedule, ride_data: RideData, user: User) -> bool:
        ride = dict(
            location=ride_data.location,
            latitude=ride_data.latitude,
            longitude=ride_data.longitude,
        )

        await user.rides.connect(schedule, ride)

        return True
