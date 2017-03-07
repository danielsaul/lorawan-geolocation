"""
    ThingServer
    Use unofficial Things Connected dashboard API to get new packets
"""

from redis import StrictRedis
from redis.exceptions import ConnectionError

import time
import requests

import settings as s

def login(session):
    resp = session.post('https://dashboard.thingsconnected.net/api/login', json={'email': s.LOGIN_EMAIL, 'password': s.LOGIN_PASSWORD})
    
    if resp.status_code != 200:
        print "Unable to login."
    else:
        print "Logged in."

    return

def loop(session,r):

    resp = session.get('https://dashboard.thingsconnected.net/api/devices/%s/messages/' % s.DEVICE)
    if resp.status_code != 200:
        login(s)

    else:
        r.publish('dashboard_messages', resp.text)

    time.sleep(s.FREQUENCY)


if __name__ == '__main__':
    session = requests.Session()
    
    r = StrictRedis(host=s.REDIS_HOST, port=s.REDIS_PORT, db=s.REDIS_DB)
    try:
        if r.ping():
            print "Redis connected."
    except ConnectionError:
        "Error: Redis server not available."
   
    login(session)
    
    while True:
        loop(session,r)
