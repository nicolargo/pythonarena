#!/usr/bin/env python

import xmlrpclib

host = "::1"
port = 61209

print "============="
print "Test good auth"
print "============="

print "Auth: begin"
s = xmlrpclib.ServerProxy('http://bibi:bobo@' + host + ':' + port)
print s
print "Auth: end"
try:
    print s.get()
except xmlrpclib.ProtocolError as err:
    print "A protocol error occurred"
    print "URL: %s" % err.url
    print "HTTP/HTTPS headers: %s" % err.headers
    print "Error code: %d" % err.errcode
    print "Error message: %s" % err.errmsg

# Print list of available methods
#~ print s.system.listMethods()
