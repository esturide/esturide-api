from fastapi import HTTPException
from jwt import InvalidSignatureError

from app.core import app
from app.core.exception.handler import custom_http_exception_handler, http_exception_handler, global_exception_handler, \
    invalid_credentials_handler
from app.core.exception import ResponseException
from app.presentation.api import root
from app.presentation.api.auth import auth
from app.presentation.api.travel_match_network_system import travels
from app.presentation.api.user_management_system import user_management_system

for _app in [app, user_management_system, travels]:
    _app.add_exception_handler(ResponseException, custom_http_exception_handler)
    _app.add_exception_handler(HTTPException, http_exception_handler)
    _app.add_exception_handler(Exception, global_exception_handler)
    _app.add_exception_handler(InvalidSignatureError, invalid_credentials_handler)



app.include_router(root)
app.include_router(auth)

app.mount("/user_management_system", user_management_system)
app.mount("/travel_match_network_system", travels)
