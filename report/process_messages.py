"""
    Process new packets
    Daniel Saul
"""

from redis import StrictRedis
from redis.exceptions import ConnectionError

import settings as s

import json
import struct
import base64
import copy

r = None

def process(msg, last_msg):
    data = json.loads(msg)
    new_last_msg = None
  
    for item in data:
       
        if new_last_msg is None:
            new_last_msg = copy.deepcopy(item)
        
        if last_msg==item:
            break
        
        try:
            payload = unpack_payload( base64.b16decode(item['payload'], True) )
            gateway = item['gw_gps']
            gateway['addr'] = item['gw_addr']
            gateway['time'] = item['gateway_time']
            gateway['rssi'] = item['rssi']

            saved_item = r.get('packet_%d' % payload['i'])
            if saved_item:
                saved_item = json.loads(saved_item)
                saved_item['gateways'].append(gateway)
                r.set('packet_%d' % payload['i'], json.dumps(saved_item))
            else:
                new_item = {'payload': payload, 'gateways':[gateway]}
                r.set('packet_%d' % payload['i'], json.dumps(new_item))
                r.rpush('packet_list', payload['i'])

            print r.get('packet_%d' % payload['i'])

        except:
            continue

    msg = json.dumps(new_last_msg)
    r.set('last_msg', msg)

    return new_last_msg
   

def unpack_payload(packed):
    # Payload Structure
    #0  int32_t lat;   
    #4  int32_t lon;
    #8  int32_t alt; 
    #12 uint16_t i;
    #14 uint8_t hour;
    #15 uint8_t mins;
    #16 uint8_t secs;
    #17 uint8_t sats;
    #18 char[] padding;

    fields = ['lat','lon','alt','i','hour','mins','secs','sats']
    unpacked_payload = list(struct.unpack('<iiiHBBBB2s', packed))
    payload = dict(zip(fields, unpacked_payload))
    payload['lat'] /= 10000000.0
    payload['lon'] /= 10000000.0
    payload['alt'] /= 1000.0
    return payload


if __name__ == '__main__':
 
    r = StrictRedis(host=s.REDIS_HOST, port=s.REDIS_PORT, db=s.REDIS_DB)
    try:
        if r.ping():
            print "Redis connected."
    except ConnectionError:
        "Error: Redis server not available."

    msg = r.get('last_msg')
    if not msg:
        last_msg = None
    else:
        last_msg = json.loads(msg)

    p = r.pubsub()
    p.subscribe('dashboard_messages')

    for message in p.listen():
        if message['type'] == 'message':
            last_msg = process(message['data'], last_msg)
