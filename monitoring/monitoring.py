"""
Tests are checking connectivity to web application and Redis, response code of web application, and value in Redis 

REDIS_ADDR should be a string like host:port for connection to Reds
APP_ADDR should be a string like host:port for connection to Web Application

Value 0 is meaning that the App or Redis is unavailable or Redis does not have the needed key
Value 1 is the opposite meaning 0
"""

from os import getenv
from time import sleep
import redis
import requests
from prometheus_client import start_http_server,Gauge

REDIS_PING      = Gauge('redis_ping', "Checking connectivity to Redis")
REDIS_MESSAGE   = Gauge('redis_message', "Checking message in Redis")
APP_STATUS_CODE = Gauge('app_status_code', "Checking status code of Web Application")

def get_metrics():
    #Initialization
    result = {}
    r = redis.Redis(host=getenv('REDIS_ADDR').split(':')[0], port=getenv('REDIS_ADDR').split(':')[1], db=0)
    url = f"http://{getenv('APP_ADDR').split(':')[0]}:{getenv('APP_ADDR').split(':')[1]}"

    #Redis ping check
    redis_ping = None
    try:
        redis_ping = r.ping()
    except redis.exceptions.ConnectionError:
        REDIS_PING.set(0)
    if redis_ping != None and redis_ping: REDIS_PING.set(1)

    #Redis check message
    redis_response = None
    try:
        redis_response = r.get('updated_time')
    except redis.exceptions.ConnectionError:
        REDIS_MESSAGE.set(0)
    REDIS_MESSAGE.set(1) if redis_response != None else REDIS_MESSAGE.set(0)

    #Application check 
    resp = None
    try:
        resp = requests.get(url)
    except requests.exceptions.ConnectionError:
        APP_STATUS_CODE.set(503)
    if hasattr(resp, 'status_code'):
        APP_STATUS_CODE.set(resp.status_code)
    else:
        APP_STATUS_CODE.set(503)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    while True:
        get_metrics()
        sleep(2.5)
