#!/usr/bin/env python

__appname__ = 'snmpget'
__version__ = "0.1"
__author__ = "Nicolas Hennion <nicolas@nicolargo.com>"
__licence__ = "LGPL"

try:
    from pysnmp.entity.rfc3413.oneliner import cmdgen
except ImportError, e:
    print("Error importing PySNMP lib: %s" % e)
    print("Install using pip: # pip install pysnmp")

class snmpclient(object):
    """ SNMP client class (based on PySNMP) """
    
    def __init__(self, host = "localhost", 
                       port = 161, 
                       community = "public",
                       version = "SNMPv2-MIB"): 
        super(snmpclient, self).__init__()
        self.cmdGen = cmdgen.CommandGenerator()
        self.host = host
        self.port = port
        self.community = community
        self.version = version

    def __result__(self, errorIndication, errorStatus, errorIndex, varBinds):
        ret = {}
        if not (errorIndication or errorStatus):
            for name, val in varBinds:
                ret[name.prettyPrint()] = val.prettyPrint()
        return ret

    def get_by_oid(self, *oid):
        errorIndication, errorStatus, errorIndex, varBinds = self.cmdGen.getCmd(
            cmdgen.CommunityData(self.community),
            cmdgen.UdpTransportTarget((self.host, self.port)),
            *oid
        )
        return self.__result__(errorIndication, errorStatus, errorIndex, varBinds)


if __name__ == "__main__":
    c = snmpclient(host="demo.snmplabs.com")
    print c.get_by_oid("1.3.6.1.2.1.1.5.0", # Sysname 
                       "1.3.6.1.2.1.1.1.0",  # Uname
                       "1.3.6.1.2.1.2.2.1.2.1" # Net interface #1
                       )
