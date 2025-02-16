from app.domain.models import Schedule, User
from app.domain.types import LocationData
from app.presentation.schemes import DriverProfile, TrackingRecord
from app.presentation.schemes.travels import TravelResult


def create_travel_scheme(schedule: Schedule, driver: User, origin: LocationData, destination: LocationData):
    return TravelResult(
        uuid=schedule.uuid,

        price=schedule.price,
        active=schedule.active,
        terminate=schedule.terminate,
        cancel=schedule.cancel,
        max_passengers=schedule.max_passenger,

        driver=DriverProfile(
            code=driver.code,
            firstname=driver.firstname,
            maternal_surname=driver.maternal_surname,
            paternal_surname=driver.paternal_surname,
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
