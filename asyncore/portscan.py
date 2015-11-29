# -*- coding: utf-8 -*-
#
# POC for the new Port scanner plugin (Glances)
# Nicolargo (11/2015)
#

import asyncore
import socket

class PortScanner(asyncore.dispatcher):

    def __init__(self, host, port):
        self.host = host
        self.port = port

        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connect((host, port))
        except Exception as e:
            print 'Connection error for %s:%s (%s)' % (self.host, self.port, e)
            self.close()

    def handle_connect(self):
        print 'Connected to %s:%s' % (self.host, self.port)
        self.close()

scanlist = []
scanlist.append(PortScanner('www.google.fr', 443))
scanlist.append(PortScanner('www.inria.fr', 80))
scanlist.append(PortScanner('www.inria.fr', 1024))
scanlist.append(PortScanner('www.nonXXXexistingXXX.com', 80))

asyncore.loop(timeout=1, count=3)
