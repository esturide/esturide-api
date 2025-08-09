import functools

from geopy.geocoders import Nominatim
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from jwt import InvalidSignatureError

from app.core import get_root_app
from app.core.exception.handler import (
    custom_http_exception_handler,
    http_exception_handler,
    global_exception_handler,
    invalid_credentials_handler
)
from app.core.exception import ResponseException, NotFoundException
from app.presentation.api import root
from app.presentation.api.auth import auth
from app.presentation.api.health import health
from app.presentation.api.v1.user_management import get_user_management_v1
from app.presentation.api.v1.travel_match_network import get_travels_match_network_v1


@functools.lru_cache()
def get_app():
    app = get_root_app()

    for _app in [app, get_user_management_v1(), get_travels_match_network_v1()]:
        _app.add_exception_handler(ResponseException, custom_http_exception_handler)
        _app.add_exception_handler(HTTPException, http_exception_handler)
        _app.add_exception_handler(InvalidSignatureError, invalid_credentials_handler)
        _app.add_exception_handler(Exception, global_exception_handler)

    app.include_router(root)
    app.include_router(auth)
    app.include_router(health)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount("/v1/user-management", get_user_management_v1())
    app.mount("/v1/travel-match-network", get_travels_match_network_v1())

    return app
