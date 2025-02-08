import abc
import asyncio
import json

from websockets import ConnectionClosed, connect


class BaseConnect(abc.ABC):
    def __init__(self, link: str):
        self.__link = link

    @property
    def link(self) -> str:
        return self.__link

    @abc.abstractmethod
    async def on_start(self) -> dict:
        pass

    @abc.abstractmethod
    async def on_close(self):
        pass

    @abc.abstractmethod
    async def on_message(self, message: str):
        pass

    async def connect(self) -> None:
        async with connect(self.__link) as websocket:
            await websocket.send(json.dumps(await self.on_start()))
            async for m in websocket:
                try:
                    await self.on_message(m)
                except ConnectionClosed:
                    await self.on_close()
                await asyncio.sleep(1)
