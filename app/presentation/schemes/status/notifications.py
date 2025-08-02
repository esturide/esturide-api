from pydantic import BaseModel

from app.core.enum import Status


class StatusMessage(BaseModel):
    status: Status
    message: str

