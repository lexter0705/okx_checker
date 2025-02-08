import asyncio
import json
import logging

import redis

from connector.connects.base import BaseConnect


class OkxConnect(BaseConnect):
    def __init__(self, pair: str, redis_connect: redis.Redis):
        self.__pair = pair
        self.__redis_connect = redis_connect
        link = "wss://ws.okx.com/ws/v5/public"
        super().__init__(link)
        print(pair)

    async def on_close(self):
        logging.warning(f"WARNING {self.__pair} connection is closed!!!")
        await asyncio.sleep(60)
        logging.info(f"INFO reconnecting to {self.__pair}")
        await self.connect()

    async def on_message(self, message: str):
        message = json.loads(message)
        if "action" in message.keys() and message["action"] == "update":
            logging.info(f"INFO New data from {self.__pair}: {message}")
            sellers = json.loads(self.__redis_connect.get(f"{self.__pair}-sell"))
            buyers = json.loads(self.__redis_connect.get(f"{self.__pair}-buy"))
            sellers = sellers + message["data"][0]["asks"]
            buyers = buyers + message["data"][0]["bids"]
            self.__redis_connect.set(f"{self.__pair}-sell", json.dumps(sellers))
            self.__redis_connect.set(f"{self.__pair}-buy", json.dumps(buyers))
        elif "action" in message.keys() and message["action"] == "snapshot":
            sellers = message["data"][0]["asks"]
            buyers = message["data"][0]["bids"]
            self.__redis_connect.set(f"{self.__pair}-sell", json.dumps(sellers))
            self.__redis_connect.set(f"{self.__pair}-buy", json.dumps(buyers))

    async def on_start(self) -> dict:
        logging.info(f"INFO {self.__pair} starting connection")
        data = {"op": "subscribe",
                "args": [{
                    "channel": "books",
                    "instId": self.__pair,
                }]
                }
        return data
