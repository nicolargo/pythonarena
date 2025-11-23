import asyncio
from pysnmp.hlapi.v3arch.asyncio import *


async def run():
    snmpEngine = SnmpEngine()

    iterator = get_cmd(
        snmpEngine,
        CommunityData("public", mpModel=0),
        await UdpTransportTarget.create(("127.0.0.1", 161)),
        ContextData(),
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
    )

    errorIndication, errorStatus, errorIndex, varBinds = await iterator

    if errorIndication:
        print(errorIndication)

    elif errorStatus:
        print(
            "{} at {}".format(
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
            )
        )
    else:
        for varBind in varBinds:
            print(" = ".join([x.prettyPrint() for x in varBind]))

    snmpEngine.close_dispatcher()


asyncio.run(run())

