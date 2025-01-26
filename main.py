from app.core import app
from app.presentation.api import root
from app.presentation.api.auth import auth
from app.presentation.api.travel_match_network_system import travels
from app.presentation.api.user_management_system import user_management_system
from app.exception_handler import CustomAppException  , custom_exception_handler
from fastapi import FastAPI, Request  
from fastapi.responses import JSONResponse

app.include_router(root)
app.include_router(auth)

app.mount("/user_management_system", user_management_system)
app.mount("/travel_match_network_system", travels)
app.add_exception_handler(CustomAppException, custom_exception_handler)
