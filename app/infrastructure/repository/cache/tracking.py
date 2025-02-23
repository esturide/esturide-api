from typing import List

from app.core.dependencies.depends.database.redis import CacheSession
from app.core.types import UUID, UserCode
from app.domain.types import TrackingRecordData


class CacheTrackingRepository:
    @staticmethod
    async def record(cache: CacheSession, use_code: UserCode, record: TrackingRecordData) -> bool:
        return False

    @staticmethod
    async def get_record(cache: CacheSession, use_code: UserCode) -> List[TrackingRecordData]:
        return []

    @staticmethod
    async def user_is_record(cache: CacheSession, use_code: UserCode):
        pass
