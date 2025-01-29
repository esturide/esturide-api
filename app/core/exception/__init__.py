import typing


class ResponseException(Exception):
    def __init__(self, status_code: int, detail: typing.LiteralString):
        self.status_code = status_code
        self.detail = detail


class UnauthorizedAccessException(ResponseException):
    def __init__(self):
        super().__init__(status_code=401, detail="Unauthorized access")


class ForbiddenAccessException(ResponseException):
    def __init__(self):
        super().__init__(status_code=403, detail="Forbidden access")


class ResourceNotFoundException(ResponseException):
    def __init__(self):
        super().__init__(status_code=404, detail="Resource not found")


class ValidationException(ResponseException):
    def __init__(self, detail="Validation error"):
        super().__init__(status_code=422, detail=detail)


class DataAlreadyExistsException(ResponseException):
    def __init__(self, detail="The data already exists"):
        super().__init__(status_code=409, detail=detail)
        self.detail = detail
