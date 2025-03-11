from pydantic import BaseModel, Field


class FoundLocation(BaseModel):
    address: str = Field(..., title="Address", alias='address')
    longitude: float = Field(0, title="Longitude", alias='longitude')
    latitude: float = Field(0, title="Latitude", alias='latitude')


class SearchLocation(FoundLocation):
    ...
