from fastapi import Request
from fastapi.responses import JSONResponse


class CustomAppException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


class UnauthorizedAccessException(CustomAppException):
    def __init__(self):
        super().__init__(status_code=401, detail="Unauthorized access")


class ForbiddenAccessException(CustomAppException):
    def __init__(self):
        super().__init__(status_code=403, detail="Forbidden access")


class ResourceNotFoundException(CustomAppException):
    def __init__(self):
        super().__init__(status_code=404, detail="Resource not found")


class ValidationException(CustomAppException):
    def __init__(self, detail="Validation error"):
        super().__init__(status_code=422, detail=detail)


class DataAlreadyExistsException(CustomAppException):
    def __init__(self, detail="The data already exists"):
        super().__init__(status_code=409, detail=detail)
        self.detail = detail


async def custom_exception_handler(request: Request, exc: CustomAppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
