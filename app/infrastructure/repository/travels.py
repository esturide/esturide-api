import dataclasses
from typing import Tuple, List, Literal

from neomodel import db

from app.domain.models import Schedule, Record, User, Travel
from app.infrastructure.repository.user import UserRepository


@dataclasses.dataclass
class LocationData:
    location: str
    latitude: str
    longitude: str


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
    async def filter_last_travels_by_driver(code: int, limit: int = 16) -> List[Schedule]:
        query = f"""
        MATCH (p: User)-[r: DRIVER_TO]->(c: Schedule) 
            WHERE p.code = {code} 
            RETURN c
            ORDER BY r.time 
            DESC LIMIT {limit}
        """
        results, meta = db.cypher_query(query)

        return [
            Schedule.inflate(row[0])
            for row in results]

    @staticmethod
    async def create(
            code: int,
            max_passengers: int,
            price: int,
            start: LocationData,
            end: LocationData,
    ):
        status, user = await UserRepository.get_user_by_code(code)

        if not status:
            return False, None

        start_record = Record(
            location=start.location,
            latitude=start.latitude,
            longitude=start.longitude,
        )

        end_record = Record(
            location=end.location,
            latitude=end.latitude,
            longitude=end.longitude,
        )

        schedule = await Schedule(
            max_passengers=max_passengers,
            price=price,
        ).save()

        try:
            await schedule.origin.connect(await start_record.save())
            await schedule.destination.connect(await end_record.save())

            await schedule.save()
        except Exception as e:
            raise e
        else:
            await user.schedules.connect(schedule)

        return status, schedule

    @staticmethod
    async def tracking_user(
            code: int,
            tracking: LocationData
    ):
        ...
