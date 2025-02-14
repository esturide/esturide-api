import json
import typing

from pydantic import BaseModel

C = typing.TypeVar("C")


class StreamSSE(typing.Generic[C]):
    def __init__(self) -> None:
        pass

    def send(self, data: C | dict | str) -> str:
        if isinstance(data, BaseModel):
            return self.send_model(data)
        elif isinstance(data, dict):
            return self.send_json(data)
        elif isinstance(data, str):
            return self.send_string(data)

        return str(data)

    def send_model(self, model: C)-> str:
        return json.dumps(model.model_dump())

    def send_json(self, data: dict)-> str:
        return json.dumps(data)

    def send_string(self, string: str) -> str:
        return string
