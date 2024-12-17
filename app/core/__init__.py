import contextlib

from fastapi import FastAPI
from fastapi_cors import CORS

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

origins = ["*"]

app.add_middleware(
    CORS,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
