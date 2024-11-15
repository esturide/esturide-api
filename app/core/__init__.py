import contextlib

import neomodel
import neomodel.config
from fastapi import FastAPI

from app.core.conf import DefaultSettings, settings

DEFAULT_APP_NAME = "Esturide (μ)  API"


@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI):
    neomodel.config.DATABASE_URL = settings.db_url
    neomodel.config.DATABASE_NAME = settings.db_name

    yield


app = FastAPI(
    title=DEFAULT_APP_NAME,
    lifespan=lifespan,
)
