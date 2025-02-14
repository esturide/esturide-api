from sse_starlette.sse import EventSourceResponse

from app.core.manager.sse.session import StreamSSE


class SSEConnectionManager:
    def __init__(self):
        self.__loop = None
        self.__session = StreamSSE()

    def pipeline(self, func):
        async def wrapper():
            async for msg in func():
                yield self.__session.send(msg)

        self.__loop = wrapper

        return func

    async def session(self):
        if self.__loop is not None:
            return EventSourceResponse(self.__loop())

        raise ValueError("Invalid session pipeline.")
