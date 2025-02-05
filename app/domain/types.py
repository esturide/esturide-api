import dataclasses


@dataclasses.dataclass
class LocationData:
    location: float
    latitude: float
    longitude: float

    @property
    def dump(self):
        return {
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
        }
