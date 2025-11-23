"""
Fetch scalar MIB variables (SNMPv1)
+++++++++++++++++++++++++++++++++++

Perform SNMP GET operation with the following options:

* with SNMPv1, community 'public'
* over IPv4/UDP
* to an Agent at demo.pysnmp.com:161
* for OIDs in tuple form

This script performs similar to the following Net-SNMP command:

| $ snmpget -v1 -c public -ObentU demo.pysnmp.com 1.3.6.1.2.1.1.1.0 1.3.6.1.2.1.1.3.0

"""  
from pysnmp.carrier.asyncio.dispatch import AsyncioDispatcher
from pysnmp.carrier.asyncio.dgram import udp, udp6
from pyasn1.codec.ber import encoder, decoder
from pysnmp.proto import api
from pysnmp.proto.rfc1905 import ResponsePDU

# Protocol version to use
pMod = api.PROTOCOL_MODULES[api.SNMP_VERSION_1]
# pMod = api.PROTOCOL_MODULES[api.SNMP_VERSION_2C]

# Build PDU
reqPDU = pMod.GetRequestPDU()
pMod.apiPDU.set_defaults(reqPDU)
pMod.apiPDU.set_varbinds(
    reqPDU, (("1.3.6.1.2.1.1.1.0", pMod.Null("")), ("1.3.6.1.2.1.1.3.0", pMod.Null("")))
)

# Build message
reqMsg = pMod.Message()
pMod.apiMessage.set_defaults(reqMsg)
pMod.apiMessage.set_community(reqMsg, "public")
pMod.apiMessage.set_pdu(reqMsg, reqPDU)


# noinspection PyUnusedLocal,PyUnusedLocal
def cbRecvFun(
    transportDispatcher, transportDomain, transportAddress, wholeMsg, reqPDU=reqPDU
):
    while wholeMsg:
        rspMsg, wholeMsg = decoder.decode(wholeMsg, asn1Spec=pMod.Message())
        rspPDU: ResponsePDU = pMod.apiMessage.get_pdu(rspMsg)

        # Match response to request
        if pMod.apiPDU.get_request_id(reqPDU) == pMod.apiPDU.get_request_id(rspPDU):
            # Check for SNMP errors reported
            errorStatus = pMod.apiPDU.get_error_status(rspPDU)
            if errorStatus:
                print(errorStatus.prettyPrint())

            else:
                for oid, val in pMod.apiPDU.get_varbinds(rspPDU):
                    print(f"{oid.prettyPrint()} = {val.prettyPrint()}")

            transportDispatcher.job_finished(1)

    return wholeMsg


transportDispatcher = AsyncioDispatcher()

transportDispatcher.register_recv_callback(cbRecvFun)

# UDP/IPv4
transportDispatcher.register_transport(
    udp.DOMAIN_NAME, udp.UdpAsyncioTransport().open_client_mode()
)

# Pass message to dispatcher
transportDispatcher.send_message(
    encoder.encode(reqMsg), udp.DOMAIN_NAME, ("demo.pysnmp.com", 161)
)
transportDispatcher.job_started(1)

## UDP/IPv6 (second copy of the same PDU will be sent)
# transportDispatcher.register_transport(
#    udp6.domainName, udp6.Udp6AsyncioTransport().open_client_mode()
# )

# Pass message to dispatcher
# transportDispatcher.send_message(
#    encoder.encode(reqMsg), udp6.domainName, ('::1', 161)
# )
# transportDispatcher.job_started(1)

# Dispatcher will finish as job#1 counter reaches zero
transportDispatcher.run_dispatcher(3)

transportDispatcher.close_dispatcher()
