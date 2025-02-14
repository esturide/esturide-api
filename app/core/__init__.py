import contextlib

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app.core.conf import DefaultSettings, settings
from app.core.dependencies.depends.database.neo4j import get_db
from app.core.dependencies.depends.database.redis import get_cache
from app.core.enum import Status

DEFAULT_APP_NAME = "Esturide (μ) API"


@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI):
    db = get_db()
    redis = get_cache()

    yield

    await redis.quit()


app = FastAPI(
    title=DEFAULT_APP_NAME,
    lifespan=lifespan,
)

origins = [
    "localhost",
    "localhost:8000",
    "localhost:80",
    "127.0.0.1:8000",
    "0.0.0.0:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
    compresslevel=5
)
