#!/usr/bin/env python

from twisted.internet.protocol import Protocol, ServerFactory
from twisted.internet import reactor
import json
import zlib
import psutil
import time

### Protocol Implementation

class GlancesServer(Protocol):
    
    connectionNb = 0
    
    def __init__(self):
        pass
    
    def connectionMade(self):
        self.connectionNb += 1
        print "New connection: ", format(self.connectionNb)

    def dataReceived(self, rcvdata):
        print "Data received: ", format(rcvdata)
        if rcvdata == "QUIT":
            self.transport.loseConnection()
        else:
            snddata = psutil.cpu_percent(interval=1, percpu=True)        
            self.transport.write(zlib.compress(json.dumps(snddata)))
            self.transport.write(rcvdata)            

    def connectionLost(self, reason):
        self.connectionNb -= 1
        print "End connection: ", reason.getErrorMessage()


class GlancesServerFactory(ServerFactory):
    
    protocol = GlancesServer

def main():
    port = 61209    
    reactor.listenTCP(port, GlancesServerFactory())
    #~ time.sleep(10)
    reactor.run()

if __name__ == '__main__':
    main()
