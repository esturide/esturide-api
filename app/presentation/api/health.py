from fastapi import APIRouter

from app.core.dependencies.database import DependCache, DependDatabase
from app.core.types import Status
from app.presentation.schemes import StatusMessage

health = APIRouter(
    prefix="/health",
    tags=["Check health service"]
)


@health.get('/db', response_model=StatusMessage)
async def check_db_connection(db: DependDatabase):
    db.cypher_query("RETURN 'Hello World' as message")

    return {
        "status": Status.success,
        "message": "Can connect to database."
    }


@health.get('/cache', response_model=StatusMessage)
async def check_cache_connection(cache: DependCache):
    await cache.set('test_key', 'Hello, Redis!')
    await cache.get('test_key')

    return {
        "status": Status.success,
        "message": "Can connect to cache."
    }
