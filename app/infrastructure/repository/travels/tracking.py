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

        return results and data_json in results[0][0]

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

        return results and data_json in results[0][0]
