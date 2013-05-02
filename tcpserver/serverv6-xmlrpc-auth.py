#!/usr/bin/env python

from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from base64 import b64decode
import SocketServer
import socket
import psutil

host = "::0"
port = 61209

# The GET function


def get():
    return psutil.cpu_percent(interval=1, percpu=True)


# Server definition

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

    def authenticate(self, headers):
        headers.get('Authorization')
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


class SimpleThreadedXMLRPCServer(SocketServer.ThreadingMixIn,
                                 SimpleXMLRPCServer):

    def __init__(self, bind_addrport):
        # Create server
        self.server = SimpleXMLRPCServer(bind_addrport,
                                         requestHandler=RequestHandler)
        self.server.register_introspection_functions()
        self.server.register_function(get, 'get')

    def serve_forever(self):
        self.server.serve_forever()

    def server_close(self):
        self.server.server_close()

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET,
                               socket.SO_REUSEADDR, 1)
        SimpleXMLRPCServer.server_bind(self)


class MyServer(SimpleThreadedXMLRPCServer):

    address_family = socket.AF_INET6


if __name__ == "__main__":
    if socket.has_ipv6:
        print("IPv6 Socket supported on your system")
    server = MyServer((host, port))
    server.serve_forever()
