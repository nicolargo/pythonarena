#!/usr/bin/env python

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import psutil

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("localhost", 61209),
                            requestHandler=RequestHandler)
server.register_introspection_functions()

# Register the GET function
def get():
    return psutil.cpu_percent(interval=1, percpu=True)
server.register_function(get, 'get')

#~ # Register an instance; all the methods of the instance are
#~ # published as XML-RPC methods (in this case, just 'div').
#~ class MyFuncs:
    #~ def div(self, x, y):
        #~ return x // y
#~ server.register_instance(MyFuncs())

# Run the server's main loop
server.serve_forever()
