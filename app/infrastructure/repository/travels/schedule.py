from typing import Tuple, List, Literal

from fastapi import HTTPException
from neomodel import db

from app.core.types import UserCode
from app.domain.models import Schedule, User, Travel
from app.domain.types import LocationData
from app.infrastructure.repository.user import UserRepository


class ScheduleRepository:
    @staticmethod
    async def get(**kwargs) -> Tuple[Literal[False], None] | Tuple[Literal[True], Schedule]:
        node = await Schedule.nodes.get_or_none(**kwargs)

        if node is None:
            return False, None

        return True, node

    @staticmethod
    async def get_all(limit: int = 16, **kwargs) -> List[Schedule]:
        all_travels = [*await Schedule.nodes.all()]

        return all_travels[:limit]

    @staticmethod
    async def filter_ordered_time(limit: int = 16) -> List[Tuple[Schedule, Travel, User]]:
        query = f"""
        MATCH (p: User)-[r: DRIVER_TO]->(c: Schedule) 
            RETURN c, r, p 
            ORDER BY r.time DESC 
            LIMIT {limit}
        """
        results, meta = db.cypher_query(query)

        return [(
            Schedule.inflate(row[0]),
            Travel.inflate(row[1]),
            User.inflate(row[2])
        ) for row in results]

    @staticmethod
    async def filter_actives(limit: int = 16) -> List[Tuple[Schedule, Travel, User]]:
        query = f"""
        MATCH (p: User)-[r: DRIVER_TO]->(c: Schedule) 
            WHERE r.active = true 
            RETURN c
            ORDER BY r.time DESC 
            LIMIT {limit}
        """
        results, meta = db.cypher_query(query)

        return [(
            Schedule.inflate(row[0])
        ) for row in results]

    @staticmethod
    async def filter_last_travels_by_driver(code: UserCode, limit: int = 16) -> List[Schedule]:
        query = f"""
        MATCH (p: User)-[r: DRIVER_TO]->(c: Schedule) 
            WHERE p.code = {code} 
            RETURN c
            ORDER BY r.time 
            DESC LIMIT {limit}
        """
        results, meta = db.cypher_query(query)

        return [Schedule.inflate(row[0]) for row in results]

    @staticmethod
    async def get_active_travel(code: UserCode, limit: int = 3) -> Schedule:
        query = f"""
        MATCH (p: User)-[r: DRIVER_TO]->(c: Schedule) 
            WHERE p.code = {code} AND c.cancel = false AND c.terminate = false OR c.active = true
            RETURN c
            ORDER BY r.time 
            DESC LIMIT {limit}
        """
        results, meta = db.cypher_query(query)

        schedules = [Schedule.inflate(row[0]) for row in results]

        if len(schedules) <= 0:
            raise HTTPException(status_code=404, detail="No active travels found.")

        return schedules[0]

    @staticmethod
    async def create(
            code: UserCode,
            max_passengers: int,
            price: int,
            start: LocationData,
            finished: LocationData,
    ):
        status, user = await UserRepository.get_user_by_code(code)

        if not status:
            return False, None

        schedule = await Schedule(
            max_passengers=max_passengers,
            price=price,
            start=start.dump,
            finished=finished.dump,
        ).save()

        try:
            await schedule.save()
        except Exception as e:
            raise e
        else:
            await user.schedules.connect(schedule)

        return status, schedule

    @staticmethod
    async def tracking_user(
            code: UserCode,
            tracking: LocationData
    ):
        ...
