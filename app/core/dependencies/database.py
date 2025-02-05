from typing import Annotated

from fastapi import Depends

from app.core.dependencies.depends.database.neo4j import get_db, DatabaseSession
from app.core.dependencies.depends.database.redis import get_cache, CacheSession

DependCache = Annotated[CacheSession, Depends(get_cache)]
DependDatabase = Annotated[DatabaseSession, Depends(get_db)]
