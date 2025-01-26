from fastapi.responses import JSONResponse

from app.core.types import Status
from app.presentation.schemes import StatusMessage


async def exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def http_exception_handler(request, exc):
    if exc.status_code in [400, 401, 403, 404, 406, 422]:
        error_response = StatusMessage(
            status=Status.failure,
            message=str(exc.detail)
        )

        return JSONResponse(status_code=200, content=error_response.model_dump())

    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )
