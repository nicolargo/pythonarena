#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Testbed for a ps + net top command
# Nicolas Hennion (@nicolargo)
# 02/2017
#
# Externals libs: psutil
#
# !!! Lot's of restrictions (see __init__ function)
#

import psutil
import socket
from struct import unpack


class Packet():

    def __init__(self):
        # 1) Want to try socket.IPPROTO_IP ?
        # This will not work, since IPPROTO_IP is a dummy protocol not a real one.
        # Had to do the same kind of thinks with IPPROTO_UDP and IPPROTO_ICMP
        # 2) Only incoming trafic will be capture
        # 3) Ethernet headers is not available
        self._socket = socket.socket(socket.AF_INET,
                                     socket.SOCK_RAW,
                                     socket.IPPROTO_TCP)
        self._raw = None
        self._net_connections = []
        self._ip_header = None

    def receive(self):
        """Receive a new packet"""
        self._raw = self._socket.recvfrom(65535)[0]

        # Get the processes net stats
        self._net_connections = psutil.net_connections(kind='tcp')

        # Unpack the packet
        self._ip_header = unpack('!BBHHHBBH4s4s', self._raw[0:20])
        if self.ip_protocol() == 6:
            # TCP
            tcp_header_start = self.ip_header_length() * 4
            self._tcp_header = unpack('!HHLLBBHHH',
                                      self._raw[tcp_header_start:tcp_header_start + 20])
            tcp_data_start = tcp_header_start + self.tcp_header_length() * 4
            self._tcp_data = self._raw[tcp_data_start:]
        return True

    def ip_header(self):
        """Unpack the IP header (first 20 bytes of the packet)"""
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

    def pid(self):
        """Try to find the relative process PID"""
        for p in self._net_connections:
            if p.laddr[0] == self.ip_destination() \
               and p.laddr[1] == self.tcp_destination_port() \
               and p.raddr[0] == self.ip_source() \
               and p.raddr[1] == self.tcp_source_port():
                return p.pid
        return None


def main():
    p = Packet()
    for i in xrange(1, 100):
        p.receive()
        print('=' * 80)
        print('IP version           = {}'.format(p.ip_version()))
        print('IP header length     = {}'.format(p.ip_header_length()))
        print('IP TTL               = {}'.format(p.ip_ttl()))
        print('IP protocol          = {}'.format(p.ip_protocol()))
        print('IP source            = {}'.format(p.ip_source()))
        print('IP destination       = {}'.format(p.ip_destination()))
        print('TCP header length    = {}'.format(p.tcp_header_length()))
        print('TCP source port      = {}'.format(p.tcp_source_port()))
        print('TCP destination port = {}'.format(p.tcp_destination_port()))
        print('TCP data length      = {}'.format(p.tcp_data_length()))
        print('Packet size          = {}'.format(p.size()))
        print('PID                  = {}'.format(p.pid()))
        print('Process name         = {}'.format(psutil.Process(p.pid()).name))


if __name__ == '__main__':
    main()
