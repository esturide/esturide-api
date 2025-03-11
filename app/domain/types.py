import dataclasses


@dataclasses.dataclass
class LocationData:
    latitude: float
    longitude: float

    @property
    def dump(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
        }
