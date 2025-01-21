from fastapi import HTTPException, Request
from starlette.responses import JSONResponse

from app.core import app
from app.core.types import Status
from app.presentation.api import root
from app.presentation.api.auth import auth
from app.presentation.api.travel_match_network_system import travels
from app.presentation.api.user_management_system import user_management_system
from app.presentation.schemes import StatusMessage

app.include_router(root)
app.include_router(auth)

app.mount("/user_management_system", user_management_system)
app.mount("/travel_match_network_system", travels)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code in [400, 401, 403, 404, 406, 422]:
        error_response = StatusMessage(
            status=Status.failure,
            message=str(exc.detail)
        )

        return JSONResponse(status_code=200, content=error_response.model_dump())

    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )
