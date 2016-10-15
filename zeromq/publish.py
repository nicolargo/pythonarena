# -*- coding: utf-8 -*-
#
# POC for ZeroMQ
# Nicolargo (10/2016)
#

import json
import zmq
import time

c = zmq.Context()

publisher = c.socket(zmq.PUB)
publisher.bind("tcp://127.0.0.1:5678")

key = 'G'

while True:
    # Add the enveloppe
    data = [key, 'plugin', json.dumps({'a': 1, 'b': 2})]
    publisher.send_multipart(data)
    time.sleep(1)
