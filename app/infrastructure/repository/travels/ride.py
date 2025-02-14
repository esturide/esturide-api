from typing import Tuple, Literal

from fastapi import HTTPException
from neomodel import DoesNotExist, db

from app.core.types import UserCode
from app.domain.models import Schedule, User, Ride
from app.domain.types import RideData


class RideRepository:
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
    async def get_active_ride(code: UserCode, limit: int = 16) -> Ride:
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
            raise HTTPException(status_code=404, detail="No active rides found.")

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
    async def create(schedule: Schedule, ride_data: RideData, user: User) -> bool:
        await user.rides.connect(schedule, {
            "location": ride_data.location,
            "latitude": ride_data.latitude,
            "longitude": ride_data.longitude,
        })

        return True
