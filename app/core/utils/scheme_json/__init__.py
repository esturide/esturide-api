from typing import List, Tuple

from app.domain.models import Schedule, User, Ride
from app.domain.types import LocationData
from app.presentation.schemes import TrackingRecord
from app.presentation.schemes.travels import TravelScheduleResponse, DriverUser, PassengerUser


def create_travel_scheme(
        schedule: Schedule,
        driver: User, origin:
        LocationData, destination:
        LocationData,
        users: List[Tuple[User, LocationData]]
) -> TravelScheduleResponse:
    return TravelScheduleResponse(
        uuid=schedule.uuid,

        price=schedule.price,
        active=schedule.active,
        terminate=schedule.terminate,
        cancel=schedule.cancel,
        max_passengers=schedule.max_passenger,
        passengers=[
            PassengerUser(
                code=user.code,
                firstname=user.firstname,
                maternalSurname=user.maternal_surname,
                paternalSurname=user.paternal_surname,
                position=TrackingRecord(
                    location=tracking.location,
                    latitude=tracking.latitude,
                    longitude=tracking.longitude,
                )
            ) for (user, tracking) in users
        ],

        starting=schedule.start_time,
        finished=schedule.end_time,

        seats=schedule.seats,

        driver=DriverUser(
            code=driver.code,
            firstname=driver.firstname,
            maternalSurname=driver.maternal_surname,
            paternalSurname=driver.paternal_surname,
        ),

        origin=TrackingRecord(
            location=origin.location,
            latitude=origin.latitude,
            longitude=origin.longitude,
        ),

        destination=TrackingRecord(
            location=destination.location,
            latitude=destination.latitude,
            longitude=destination.longitude,
        ),
    )
