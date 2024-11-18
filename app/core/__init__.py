import contextlib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

origins = [
    "localhost:80",
    "127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
