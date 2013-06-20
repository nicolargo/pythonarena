#!/usr/bin/env python

from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import socket
from base64 import b64decode
import psutil

# The GET function


def get():
    return psutil.cpu_percent(interval=1, percpu=True)


# Server definition

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

    def authenticate(self, headers):
        try:
            (basic, _, encoded) = headers.get('Authorization').partition(' ')
        except:
            print "No Auth"
            # Client did not ask for authentication
            return 1
        else:
            print "Auth"
            # Client authentication
            (basic, _, encoded) = headers.get('Authorization').partition(' ')
            assert basic == 'Basic', 'Only basic authentication supported'
            #    Encoded portion of the header is a string
            #    Need to convert to bytestring
            encodedByteString = encoded.encode()
            #    Decode Base64 byte String to a decoded Byte String
            decodedBytes = b64decode(encodedByteString)
            #    Convert from byte string to a regular String
            decodedString = decodedBytes.decode()
            #    Get the username and password from the string
            (username, _, password) = decodedString.partition(':')
            #    Check that username and password match internal dictionary
            print "Username: %s" % username
            print "Password: %s" % password
            if username == 'bibi' and password == 'bobo':
                return 1
            else:
                return 0

    def parse_request(self):
        if SimpleXMLRPCRequestHandler.parse_request(self):
            # next we authenticate
            if self.authenticate(self.headers):
                return True
            else:
                # if authentication fails, tell the client
                self.send_error(401, 'Authentication failed')
        return False


class MyServer(SimpleXMLRPCServer):
    address_family = socket.AF_INET6

    def __init__(self, bind_addressport, RequestHandler):
        # Create server
        self.server = SimpleXMLRPCServer(bind_addressport,
                                         requestHandler=RequestHandler)

    def server_bind(self):
        # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, False)
        SimpleXMLRPCServer.server_bind(self)

    def register(self):
        self.server.register_function(get, 'get')

    def serve_forever(self):
        self.server.serve_forever()


if __name__ == "__main__":
    server = MyServer(('', 61209), RequestHandler)
    server.register()
    server.serve_forever()
