from typing import List

from app.core.dependencies.depends.database.redis import CacheSession
from app.core.types import UUID
from app.domain.types import LocationData


class CacheTrackingRepository:
    @staticmethod
    async def record(cache: CacheSession, uuid: UUID, record: LocationData) -> bool:
        return False

    @staticmethod
    async def get_record(cache: CacheSession, uuid: UUID) -> List[LocationData]:
        return []
