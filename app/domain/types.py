import dataclasses
from datetime import datetime


@dataclasses.dataclass
class LocationData:
    location: float # Remove!
    latitude: float
    longitude: float

    @property
    def dump(self):
        return {
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
        }


@dataclasses.dataclass
class TrackingRecordData:
    latitude: float
    longitude: float
    time_record: datetime

    @property
    def dump(self):
        return self.__dict__
