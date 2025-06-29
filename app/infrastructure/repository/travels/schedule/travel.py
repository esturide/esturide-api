from neomodel import db

from app.core.exception import NotFoundException
from app.domain.models import Schedule, Travel, User


class TravelRepository:
    @staticmethod
    async def get(schedule: Schedule, user: User) -> Travel:
        query = f"""
        MATCH (p: User)-[r: DRIVER_TO]->(c: Schedule) 
            WHERE p.code = $user AND c.uuid = $schedule
            RETURN r
            ORDER BY r.time 
            DESC LIMIT 1
        """
        results, meta = db.cypher_query(query, {'user': user.code, 'schedule': schedule.uuid})

        travels = [Travel.inflate(row[0]) for row in results]

        if len(travels) <= 0:
            raise NotFoundException(detail="Travel not found.")

        return travels[0]
