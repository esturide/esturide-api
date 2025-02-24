
from sse_starlette.sse import EventSourceResponse

from app.core.manager.sse.session import StreamSSE
from app.core.types import CallableAsyncGenerator


class SSEConnectionManager:
    def __init__(self):
        self.__loop = None
        self.__session = StreamSSE()

    def pipeline(self, func: CallableAsyncGenerator) -> CallableAsyncGenerator:
        async def wrapper_func(*args, **kwargs):
            _session = StreamSSE()

            async for msg in func(*args, **kwargs):
                print(msg)
                yield _session.send(msg)

        return wrapper_func

    async def session(self):
        if self.__loop is not None:
            return EventSourceResponse(self.__loop())

        raise ValueError("Invalid session pipeline.")
