from typing import List

from app.core.dependencies.depends.database.redis import CacheSession
from app.core.types import UUID
from app.domain.types import LocationData, TrackingRecordData
from app.infrastructure.repository.cache.tracking import CacheTrackingRepository
from app.infrastructure.repository.travels.tracking import StaticTrackingRepository


class TrackingService:
    async def record_to_cache(self, cache: CacheSession, uuid: UUID, record: TrackingRecordData) -> bool:
        status = await CacheTrackingRepository.record(cache, uuid, record)

        return status

    async def get_records_from_cache(self, cache: CacheSession, uuid: UUID) -> List[LocationData]:
        return []

    async def save_data_to_database_from_driver(self, cache: CacheSession, uuid: UUID) -> bool:
        return False

    async def save_data_to_database_from_passenger(self, cache: CacheSession, uuid: UUID) -> bool:
        return False

    async def get_records_from_data(self, uuid: UUID) -> List[TrackingRecordData]:
        return await StaticTrackingRepository.get_all_record_from_uuid(uuid)
