import logging
from threading import Thread

import redis
import uvicorn

from connector import OkxConnectCreator, OkxPairGetter
from server.app import app



def start_websocket_connects():
    redis_connect = redis.Redis(host='localhost', port=6379, db=0)
    logging.basicConfig(filename="logs/app.log", level=logging.INFO)
    getter = OkxPairGetter()
    all_pairs = getter.get_all_pairs()
    creator = OkxConnectCreator(redis_connect)
    creator.create_connects(all_pairs)


def start_server():
    uvicorn.run(app, host='127.0.0.1', port=8000)


if __name__ == '__main__':
    thread_one = Thread(target=start_websocket_connects)
    thread_one.start()
    thread_two = Thread(target=start_server)
    thread_two.start()
    thread_two.join()
    thread_one.join()
