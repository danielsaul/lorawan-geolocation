# -*- coding: utf-8 -*-
"""
    ThingServer
    Integrate with the EveryNet Core API for LoRaWAN.
"""

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher

import json

from base64 import b64encode

@dispatcher.add_method
def uplink(**kwargs):
    print "uplink"
    with open('uplink.json', 'a') as f:
        json.dump(kwargs, f)
        f.write("\n")
    return "ok"

@dispatcher.add_method
def post_uplink(**kwargs):
    print "post_uplink"
    with open('post_uplink.json', 'a') as f:
        json.dump(kwargs, f)
        f.write("\n")
    return "ok"

@dispatcher.add_method
def downlink(**kwargs):
#    reply = { "payload": b64encode("ACK") }
#    return reply
    return

@Request.application
def application(request):
    response = JSONRPCResponseManager.handle(
        request.get_data(cache=False, as_text=True), dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('0.0.0.0', 8080, application)
