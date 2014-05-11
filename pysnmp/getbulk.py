#!/usr/bin/env python

__appname__ = 'snmpbulk'
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

    def __bulk_result__(self, errorIndication, errorStatus, errorIndex, varBindTable):
        ret = []
        if not (errorIndication or errorStatus):
            for varBindTableRow in varBindTable:
                item = {}
                for name, val in varBindTableRow:
                    if (str(val) == ''):
                        item[name.prettyPrint()] = ''
                    else:
                        item[name.prettyPrint()] = val.prettyPrint()
                ret.append(item)
        return ret

    def getbulk_by_oid(self, non_repeaters, max_repetitions, *oid):
        errorIndication, errorStatus, errorIndex, varBindTable = self.cmdGen.bulkCmd(
            cmdgen.CommunityData(self.community),
            cmdgen.UdpTransportTarget((self.host, self.port)),
            non_repeaters, 
            max_repetitions,
            *oid
        )
        return self.__bulk_result__(errorIndication, errorStatus, errorIndex, varBindTable)


if __name__ == "__main__":
    c = snmpclient(host='demo.snmplabs.com')
    print c.getbulk_by_oid(0, 25, 
                           '1.3.6.1.2.1.2.2.1.2', 
                           '1.3.6.1.2.1.2.2.1.10',
                           '1.3.6.1.2.1.2.2.1.16')
