from neo4j import GraphDatabase
from neomodel import db
from neomodel import config
from neomodel.sync_.core import Database


def connect_db(settings) -> Database:
    config.DATABASE_URL = settings.db_url
    config.DATABASE_NAME = settings.db_name

    return db
