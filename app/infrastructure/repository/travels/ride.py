import json
from typing import Tuple, Literal

from fastapi import HTTPException
from neomodel import DoesNotExist, db

from app.core.exception import NotFoundException
from app.core.types import UserCode, UUID
from app.domain.models import Schedule, User, Ride
from app.domain.types import LocationData


class RideRepository:
    @staticmethod
    async def update_tracking(uuid: UUID, tracking: LocationData):
        data_json = json.dumps(tracking.__dict__)

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
    async def get(schedule: Schedule, passenger: User) -> Tuple[Literal[False], None] | Tuple[Literal[True], Ride]:
        try:
            ride = await passenger.rides.relationship(schedule)

            if ride is None:
                return False, None

        except DoesNotExist:
            return False, None
        else:
            return True, ride

    @staticmethod
    async def get_by_uuid(uuid: UUID) -> Ride:
        query = f"""
        MATCH (p: User)-[r: RIDE_TO]->(c: Schedule) 
            WHERE r.uuid = '{uuid}'
            RETURN r
        """
        results, meta = db.cypher_query(query)

        rides = [Ride.inflate(row[0]) for row in results]

        if len(rides) <= 0:
            raise NotFoundException(detail="Ride not found.")

        return rides[0]

    @staticmethod
    async def get_active_ride(code: UserCode, limit: int = 1) -> Ride:
        query = f"""
        MATCH (p: User)-[r: RIDE_TO]->(c: Schedule) 
            WHERE p.code = {code} AND c.active = true AND r.cancel = false
            RETURN c
            ORDER BY r.time 
            DESC LIMIT {limit}
        """
        results, meta = db.cypher_query(query)

        schedules = [Schedule.inflate(row[0]) for row in results]

        if len(schedules) <= 0:
            raise NotFoundException(detail="No active rides found.")

        return schedules[0]

    @staticmethod
    async def get_all(schedule: Schedule):
        passengers = await schedule.passengers.all()

        rides = []

        for passenger in passengers:
            _, ride = await RideRepository.get(schedule, passenger)
            rides.append(ride)

        return rides

    @staticmethod
    async def create(schedule: Schedule, user: User) -> bool:
        await user.rides.connect(schedule, {})

        return True
