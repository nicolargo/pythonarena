#!/usr/bin/env python

from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import sys
import json
import zlib
import sys

class GlancesClient(LineReceiver):

    msg_init = "INIT"
    msg_get  = "GET"
    msg_quit = "QUIT"

    def __init__(self):
        self.connectionNb = 0

    def connectionMade(self):
        self.sendLine(self.msg_init)

    def lineReceived(self, line):
        if line == self.msg_quit:
            self.transport.loseConnection()
        else:
            rcvdata = zlib.decompress(line)
            print "Receive:", format(rcvdata)
                                    
    def sendMessage(self, msg):
        self.transport.write(msg)
        
        
class GlancesClientFactory(ClientFactory):
    
    protocol = GlancesClient

    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        return GlancesClient()

    def clientConnectionLost(self, connector, reason):
        print 'Connection lost:', reason.getErrorMessage()
        #~ reactor.stop()
        #~ Or try to reconnect
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed:', reason.getErrorMessage()
        reactor.stop()


def GlancesCallback(p):
    p.sendMessage("Hello")
    reactor.callLater(3, p.sendMessage, "This is sent in 3 second")
    reactor.callLater(6, p.sendMessage, "QUIT")
    reactor.stop()
    

def main():
    host, port = "localhost", 61209
    factory = GlancesClientFactory()
    reactor.connectTCP(host, port, factory)    
    reactor.run()


if __name__ == '__main__':
    main()
