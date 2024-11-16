import contextlib

from fastapi import FastAPI

from app.core.conf import DefaultSettings, settings
from app.core.db import connect_db

DEFAULT_APP_NAME = "Esturide (μ) API"


@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI):
    connect_db(settings)

    yield


app = FastAPI(
    title=DEFAULT_APP_NAME,
    lifespan=lifespan,
)