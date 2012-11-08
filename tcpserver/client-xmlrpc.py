#!/usr/bin/env python

import xmlrpclib

s = xmlrpclib.ServerProxy('http://localhost:61209')
print s.get()

# Print list of available methods
print s.system.listMethods()
