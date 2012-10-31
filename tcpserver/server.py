#!/usr/bin/env python

import SocketServer
import json
import zlib
import psutil
import logging

class MyTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        # Get command from the client
        self.data = self.request.recv(1024)
        print "{} wrote:".format(self.client_address[0]), format(self.data)
        # Send data to the client
        self.datatosend = psutil.cpu_percent(interval=1, percpu=True)
        print self.datatosend        
        self.request.sendall(zlib.compress(json.dumps(self.datatosend)))        
        return


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 61209
    
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
