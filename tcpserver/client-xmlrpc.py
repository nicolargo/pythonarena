#!/usr/bin/env python

import xmlrpclib

#s = xmlrpclib.ServerProxy('http://localhost:61209')
s = xmlrpclib.ServerProxy('http://192.168.1.14:61209')
print s.getAll()

# Print list of available methods
print s.system.listMethods()
