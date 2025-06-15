from pydantic import BaseModel


class FoundLocation(BaseModel):
    address: str
    longitude: float = 0
    latitude: float = 0
