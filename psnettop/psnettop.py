#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Testbed for a ps + net top command
# Nicolas Hennion (@nicolargo)
# 02/2017
#
# Externals libs: psutil
#
# Sources:
# http://www.binarytides.com/python-packet-sniffer-code-linux/
# http://askldjd.com/2014/01/15/a-reasonably-fast-python-ip-sniffer/

import psutil
import socket
from struct import unpack
from collections import namedtuple
import pprint


class Packet():

    def __init__(self):
        # 1) With socket.ntohs(0x0003), all TCP, UDP, ICMP and ARP trafic are captured
        #    We capture Ethernet packet
        # 2) Incoming and outgoing trafic are captured on the same socket
        self._socket = socket.socket(socket.AF_PACKET,
                                     socket.SOCK_RAW,
                                     socket.ntohs(3))
        self._raw = None
        self._ip_header = None

    def receive(self):
        """Receive a new packet"""
        self._raw = self._socket.recvfrom(65535)[0]

        # Unpack the packet
        self._ethernet_header = unpack('!6s6sH', self._raw[:14])
        if self.ethernet_protocol() == 8:
            # IP
            self._ip_header = unpack('!BBHHHBBH4s4s', self._raw[14:34])
            if self.ip_protocol() == 6:
                # TCP
                tcp_header_start = 14 + self.ip_header_length() * 4
                self._tcp_header = unpack('!HHLLBBHHH',
                                          self._raw[tcp_header_start:tcp_header_start + 20])
                tcp_data_start = tcp_header_start + self.tcp_header_length() * 4
                self._tcp_data = self._raw[tcp_data_start:]
        return True

    def ethernet_header(self):
        """Unpack the Ethernet header (first 14 bytes of the packet)"""
        return self._ethernet_header

    def ethernet_protocol(self):
        """Return the Ethernet protocol (8 for IP)"""
        return socket.ntohs(self._ethernet_header[2])

    def ip_header(self):
        """Unpack the IP header (20 bytes)"""
        return self._ip_header

    def ip_version(self):
        """Return the IP protocol version"""
        return self.ip_header()[0] >> 4

    def ip_header_length(self):
        """Return the IP header length """
        return self.ip_header()[0] & 0xF

    def ip_ttl(self):
        """Return the IP Time To Live"""
        return self.ip_header()[5]

    def ip_protocol(self):
        """Return the IP protocol"""
        return self.ip_header()[6]

    def ip_source(self):
        """Return the IP source adresse"""
        return socket.inet_ntoa(self.ip_header()[8])

    def ip_destination(self):
        """Return the IP destination adresse"""
        return socket.inet_ntoa(self.ip_header()[9])

    def tcp_header_length(self):
        if self.ip_protocol() == 6:
            ret = self._tcp_header[4] >> 4
        else:
            ret = None
        return ret

    def tcp_source_port(self):
        if self.ip_protocol() == 6:
            ret = self._tcp_header[0]
        else:
            ret = None
        return ret

    def tcp_destination_port(self):
        if self.ip_protocol() == 6:
            ret = self._tcp_header[1]
        else:
            ret = None
        return ret

    def tcp_data(self):
        if self.ip_protocol() == 6:
            ret = self._tcp_data
        else:
            ret = None
        return ret

    def tcp_data_length(self):
        if self.ip_protocol() == 6:
            ret = len(self._tcp_data)
        else:
            ret = None
        return ret

    def size(self):
        """Return the total packet size (with header)"""
        return len(self._raw)


class NetTopStats():

    def __init__(self):
        """Stats is a dict of dict:
        {'pid': {'bytes_recv': 27367, 'bytes_sent': 7838}}
        """
        self._stats = {}
        self._incoming = None
        self._outgoing = None

    def add_packet(self, packet):
        # Get the processes net stats
        packet_pid = self.pid(packet)
        if packet_pid is not None:
            if packet_pid not in self._stats:
                self._stats[packet_pid] = {'bytes_recv': 0, 'bytes_sent': 0}
            if self.incoming():
                self._stats[packet_pid]['bytes_recv'] += packet.size()
            elif self.outgoing():
                self._stats[packet_pid]['bytes_sent'] += packet.size()

    def pid(self, packet):
        """Try to find the relative process PID
        Also found if it is a incoming or outgoing packet"""
        self._incoming = None
        self._outgoing = None
        for p in psutil.net_connections():
            if self._match_incoming(packet, p.laddr, p.raddr):
                self._incoming = True
                return p.pid
            elif self._match_outgoing(packet, p.laddr, p.raddr):
                self._outgoing = True
                return p.pid

        return None

    def incoming(self):
        """Return True if it is an incoming packet"""
        return self._incoming is True

    def outgoing(self):
        """Return True if it is an outgoing packet"""
        return self._outgoing is True

    def _match_incoming(self, packet, laddr, raddr):
        """Check if the local laddr and remote raddr tuples (address, port)
        match the IP source/destination incoming packet"""
        return raddr != () \
            and laddr != () \
            and raddr[0] == packet.ip_source() \
            and laddr[0] == packet.ip_destination() \
            and raddr[1] == packet.tcp_source_port() \
            and laddr[1] == packet.tcp_destination_port()

    def _match_outgoing(self, packet, laddr, raddr):
        """Check if the local laddr and remote raddr tuples (address, port)
        match the IP source/destination outgoing packet"""
        return raddr != () \
            and laddr != () \
            and laddr[0] == packet.ip_source() \
            and raddr[0] == packet.ip_destination() \
            and laddr[1] == packet.tcp_source_port() \
            and raddr[1] == packet.tcp_destination_port()


def main():
    p = Packet()
    n = NetTopStats()
    while True:
        p.receive()
        n.add_packet(p)
        print('=' * 80)
        pprint.pprint(n._stats)
        # print('Ethernet protocol    = {}'.format(p.ethernet_protocol()))
        # print('IP version           = {}'.format(p.ip_version()))
        # print('IP header length     = {}'.format(p.ip_header_length()))
        # print('IP TTL               = {}'.format(p.ip_ttl()))
        # print('IP protocol          = {}'.format(p.ip_protocol()))
        # print('IP source            = {}'.format(p.ip_source()))
        # print('IP destination       = {}'.format(p.ip_destination()))
        # print('TCP header length    = {}'.format(p.tcp_header_length()))
        # print('TCP source port      = {}'.format(p.tcp_source_port()))
        # print('TCP destination port = {}'.format(p.tcp_destination_port()))
        # print('TCP data length      = {}'.format(p.tcp_data_length()))
        # print('Packet size          = {}'.format(p.size()))


if __name__ == '__main__':
    main()
