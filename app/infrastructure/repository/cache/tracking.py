from typing import List

from app.core.dependencies.depends.database.redis import CacheSession
from app.core.types import UUID
from app.domain.types import TrackingRecordData


class CacheTrackingRepository:
    @staticmethod
    async def record(cache: CacheSession, uuid: UUID, record: TrackingRecordData) -> bool:
        return False

    @staticmethod
    async def get_record(cache: CacheSession, uuid: UUID) -> List[TrackingRecordData]:
        return []
