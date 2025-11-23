import asyncio
from pysnmp.hlapi.v1arch.asyncio import *


async def run():
    with SnmpDispatcher() as snmpDispatcher:
        iterator = await get_cmd(
            snmpDispatcher,
            CommunityData("public", mpModel=0),
            await UdpTransportTarget.create(("127.0.0.1", 161)),
            ("1.3.6.1.2.1.1.1.0", None),
        )

        errorIndication, errorStatus, errorIndex, varBinds = iterator

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


asyncio.run(run())

