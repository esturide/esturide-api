import abc
import dataclasses
import json


class DataSerialize:
    @property
    @abc.abstractmethod
    def dump(self) -> dict: ...

    @property
    @abc.abstractmethod
    def serialize(self) -> str: ...


@dataclasses.dataclass
class LocationData(DataSerialize):
    latitude: float
    longitude: float

    @property
    def dump(self) -> dict:
        return self.__dict__

    @property
    def serialize(self) -> str:
        return json.dumps(self.dump)
