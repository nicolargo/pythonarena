# -*- coding: utf-8 -*-
#
# POC for ZeroMQ (Perf)
# Nicolargo (10/2016)
#

import json
import zmq
from datetime import datetime
import random
import string


def random_string(lenght):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(lenght))

c = zmq.Context()

publisher = c.socket(zmq.PUB)
publisher.setsockopt(zmq.CONFLATE, True)
publisher.setsockopt(zmq.LINGER, 0)
publisher.bind("tcp://127.0.0.1:5678")

key = 'P'

number = 22400 * 10
begin = datetime.utcnow()
for i in xrange(1, number):
    # Add the enveloppe
    data = [key,
            str(datetime.utcnow()),
            json.dumps({'mnemonic': random_string(7),
                        'eng': random_string(7),
                        'dec': random.uniform(0.0, 100.0),
                        'raw': random_string(7)})]
    publisher.send_multipart(data)
end = datetime.utcnow()

print("Publish per second: {}".format(number / (end - begin).total_seconds()))
