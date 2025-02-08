import json

import redis
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()
redis_connect = redis.Redis(host='localhost', port=6379, db=0)


@app.get("/api/buy/{pair}")
def send_buy(pair: str):
    return JSONResponse(json.loads(redis_connect.get(f"{pair}-buy")))


@app.get("/api/sell/{pair}")
def send_buy(pair: str):
    return JSONResponse(json.loads(redis_connect.get(f"{pair}-sell")))

