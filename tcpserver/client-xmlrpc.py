#!/usr/bin/env python

import xmlrpclib

s = xmlrpclib.ServerProxy('http://localhost:61209')

print "getAll"
print s.getAll()
print "getAllLimits"
print s.getAllLimits()
print "getSystem"
print s.getSystem()
print "getCore"
print s.getCore()
print "getCpu"
print s.getCpu()
print "getLoad"
print s.getLoad()
print "getMem"
print s.getMem()
print "getMemSwap"
print s.getMemSwap()
print "getSensors"
print s.getSensors()
print "getNetwork"
print s.getNetwork()
print "getDiskIO"
print s.getDiskIO()
print "getFs"
print s.getFs()
print "getProcessCount"
print s.getProcessCount()
print "getProcessList"
print s.getProcessList()
print "getNow"
print s.getNow()

# Print list of available methods
print s.system.listMethods()
