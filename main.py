from geopy.geocoders import Nominatim
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from jwt import InvalidSignatureError
from app.core import app
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
from app.presentation.api.v1.user_management import user_management_v1
from app.presentation.api.v1.travel_match_network import travels_match_network_v1


for _app in [app, user_management_v1, travels_match_network_v1]:
    _app.add_exception_handler(ResponseException, custom_http_exception_handler)
    _app.add_exception_handler(HTTPException, http_exception_handler)
    _app.add_exception_handler(InvalidSignatureError, invalid_credentials_handler)
    _app.add_exception_handler(Exception, global_exception_handler)

app.include_router(root)
app.include_router(auth)
app.include_router(health)
app.include_router(get_graphql_route(), prefix="/graphql")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/v1/user-management", user_management_v1)
app.mount("/v1/travel-match-network", travels_match_network_v1)
