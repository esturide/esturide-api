import contextlib

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app.core.conf import DefaultSettings, settings
from app.core.database.neo4j import connect_db
from app.core.enum import Status

DEFAULT_APP_NAME = "Esturide (μ) API"


@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI):
    connect_db(settings)

    yield


app = FastAPI(
    title=DEFAULT_APP_NAME,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "localhost:80",
        "127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
    compresslevel=5
)