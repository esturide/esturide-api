from functools import lru_cache

from neomodel import config
from neomodel import db
from neomodel.sync_.core import Database

from app.core.conf import get_settings

DatabaseSession = Database


def connect_db(settings) -> DatabaseSession:
    config.DATABASE_URL = settings.db_url
    config.DATABASE_NAME = settings.db_name

    return db


@lru_cache
def get_db() -> DatabaseSession:
    settings = get_settings()

    config.DATABASE_URL = settings.db_url
    config.DATABASE_NAME = settings.db_name

    return db
