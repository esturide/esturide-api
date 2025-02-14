from functools import lru_cache

from coredis import Redis

from app.core.conf import get_settings

CacheSession = Redis


@lru_cache
def get_cache() -> CacheSession:
    settings = get_settings()

    return Redis(
        host=settings.cache_host,
        port=settings.cache_port,
        db=settings.cache_databases,
        password=settings.cache_password,
    )
