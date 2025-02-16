import json
from typing import List

from neomodel import db

from app.core.types import UUID
from app.domain.types import LocationData


class StaticTrackingRepository:
    @staticmethod
    async def save_passenger_tracking_data(uuid: UUID, data: List[LocationData]) -> bool:
        data_json = str([json.dumps(tracking.__dict__) for tracking in data])

        query = f"""
        MATCH (p: User)-[r: RIDE_TO]->(c: Schedule) 
            WHERE r.uuid = '{uuid}'
            SET r.record = coalesce(r.record, []) + [$data]
            RETURN r.record AS record
        """
        results, meta = db.cypher_query(query, {
            "data": data_json
        })

        return True

    @staticmethod
    async def save_driver_tracking_data(uuid: UUID, data: List[LocationData]) -> bool:
        data_json = str([json.dumps(tracking.__dict__) for tracking in data])

        query = f"""
        MATCH (p: User)-[r: DRIVER_TO]->(c: Schedule) 
            WHERE r.uuid = '{uuid}'
            SET r.record = coalesce(r.record, []) + [$data]
            RETURN r.record AS record
        """
        results, meta = db.cypher_query(query, {
            "data": data_json
        })

        return True


    @staticmethod
    async def get_all_record_from_uuid(uuid: UUID) -> List[LocationData]:
        query = f"""
        MATCH (p: User)-[r: DRIVER_TO | RIDE_TO]->(c: Schedule) 
            WHERE r.uuid = '{uuid}'
            RETURN r.record
        """
        results, meta = db.cypher_query(query, {})

        records = [
            LocationData(**json.loads(row[0])) for row in results
        ]

        return records
