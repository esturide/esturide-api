from neomodel import db
from neomodel import config
from neomodel.sync_.core import Database


def connect_db(settings) -> Database:
    config.DATABASE_URL = settings.db_url

    return db
