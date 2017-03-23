"""
    Export data from redis
    Daniel Saul 2017
"""

from redis import StrictRedis
from redis.exceptions import ConnectionError

import settings as s

import json


if __name__ == '__main__':
 
    r = StrictRedis(host=s.REDIS_HOST, port=s.REDIS_PORT, db=s.REDIS_DB)
    try:
        if r.ping():
            print "Redis connected."
    except ConnectionError:
        "Error: Redis server not available."

    keys = r.lrange('packet_list', 0, -1)

    data = []

    for key in keys:
       value = r.get('packet_%d' % key)
       data.append(json.loads(value))

    with open('packets.json', 'w') as f:
        json.dump(data, f)
        
