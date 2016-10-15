# -*- coding: utf-8 -*-
#
# POC for the new Port scanner plugin (Glances)
# Nicolargo (11/2015)
#

import asyncore
import socket
import logging


class PortScanner(asyncore.dispatcher):

    def __init__(self, host, port=80):
        """
        """
        self.connected = None
        self.host = host
        self.port = port

        asyncore.dispatcher.__init__(self)

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.connect((host, port))
        except Exception as e:
            logging.info('Connection error for %s:%s (%s)' % (self.host, self.port, e))
            self.connected = False
            self.close()

    def handle_connect(self):
        logging.info('Connected to %s:%s' % (self.host, self.port))
        self.scan = True
        self.close()

    def handle_error(self):
        logging.info('Connection error for %s:%s' % (self.host, self.port))
        self.connected = False
        self.close()


# Build the async list
scanlist = []
scanlist.append(PortScanner('localhost', port=56339))
scanlist.append(PortScanner('localhost', port=666))
scanlist.append(PortScanner('www.google.fr', port=443))
scanlist.append(PortScanner('www.inria.fr', port=80))
scanlist.append(PortScanner('www.inria.fr', port=1024))
scanlist.append(PortScanner('www.nonXXXexistingXXX.com', port=80))

# Async loop
asyncore.loop(timeout=1, count=1)

# Print the result
res = [p.connected for p in scanlist]
print(res)
assert res == [False, False, True, True, False, False]

# Following command: is it usefull ?
[p.close() for p in scanlist]
