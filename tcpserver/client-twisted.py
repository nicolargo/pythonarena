#!/usr/bin/env python

from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import sys
import json
import zlib
import sys
import time

class GlancesClient(LineReceiver):

    msg_init = "INIT"
    msg_get  = "GET"
    msg_quit = "QUIT"

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
        #~ Try to reconnect
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed:', reason.getErrorMessage()
        reactor.stop()
    

def main():
    host, port = "localhost", 61209
    reactor.connectTCP(host, port, GlancesClientFactory())    
    reactor.run()


if __name__ == '__main__':
    main()
