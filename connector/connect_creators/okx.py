import redis
import asyncio
from connector.connect_creators.base import ConnectCreator
from connector.connects.okx import OkxConnect


class OkxConnectCreator(ConnectCreator):
    def __init__(self, redis_connect: redis.Redis):
        self.__redis_connect = redis_connect

    def create_connects(self, pairs: list[str]):
        tasks = []
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        for i in pairs[:10]:
            connect = OkxConnect(i, self.__redis_connect)
            tasks.append(loop.create_task(connect.connect()))
        loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()