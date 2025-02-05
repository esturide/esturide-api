from typing import Annotated

from fastapi import Depends

from app.core.dependencies.depends.database.neo4j import get_db, DatabaseSession
from app.core.dependencies.depends.database.redis import get_cache, CacheSession

DependCacheSession = Annotated[CacheSession, Depends(get_cache)]
DependDatabaseSession = Annotated[DatabaseSession, Depends(get_db)]
