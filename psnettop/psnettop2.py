#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Testbed for a ps + net top command version 2
# Goal of this second version: optimize CPU consumption
#
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
from Queue import Queue
import threading
import time
import signal
import sys
import pprint


class PacketSniffer(threading.Thread):

    def __init__(self):
        super(PacketSniffer, self).__init__()

        # Event needed to stop properly the thread
        self._stopper = threading.Event()

        #  Init the packets queue
        self._packets_queue = Queue()

        # 1) With socket.ntohs(0x0003), all TCP, UDP, ICMP and ARP trafic are captured
        #    We capture Ethernet packet
        # 2) Incoming and outgoing trafic are captured on the same socket
        self._socket = socket.socket(socket.AF_PACKET,
                                     socket.SOCK_RAW,
                                     socket.ntohs(3))
        self._raw = None
        self._ip_header = None

    def run(self):
        """Function called to sniff Ethernet packet
        Push packet information inside the queue
        Infinite loop, should be stopped by calling the stop() method"""
        while True:
            if self.receive():
                packet = {'source_addr': self.ip_source(),
                          'destination_addr': self.ip_destination(),
                          'source_port': self.proto_source_port(),
                          'destination_port': self.proto_destination_port(),
                          'protocol': self.ip_protocol(),
                          'size': self.size()}
                self._packets_queue.put(packet)
            if self.stopped():
                break

    def stop(self, timeout=None):
        """Stop the thread"""
        self._stopper.set()

    def stopped(self):
        """Return True is the thread is stopped"""
        return self._stopper.isSet()

    def get(self):
        """Get an item from the queue
        Return None if the queue is empty"""
        if not self._packets_queue.empty():
            return self._packets_queue.get()
        else:
            return None

    def receive(self):
        """Receive a new packet
        Return True only if it is a TCP or UDP packet"""
        self._raw = self._socket.recvfrom(65535)[0]

        # Unpack the Ethernet packet
        self._ethernet_header = unpack('!6s6sH', self._raw[:14])
        if self.ethernet_protocol() == 8:
            # Yes, it's an IP packet
            self._ip_header = unpack('!BBHHHBBH4s4s', self._raw[14:34])
            if self.ip_protocol() == 6:
                # ...and inside a TCP packet
                proto_header_size = 20
                proto_header_pack = '!HHLLBBHHH'
            elif self.ip_protocol() == 17:
                # ...and inside an UDP packet
                proto_header_size = 8
                proto_header_pack = '!HHHH'
            elif self.ip_protocol() == 1:
                # ...and inside an ICMP packet
                proto_header_size = 4
                proto_header_pack = '!BBH'
            else:
                # Ignore others packets
                return False
            proto_header_start = 14 + self.ip_header_length() * 4
            self._proto_header = unpack(proto_header_pack,
                                        self._raw[proto_header_start:proto_header_start + proto_header_size])
            proto_data_start = proto_header_start + self.proto_header_length() * 4
            self._proto_data = self._raw[proto_data_start:]
        else:
            return False
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

    def proto_header_length(self):
        if self.ip_protocol() == 6:
            # TCP
            ret = self._proto_header[4] >> 4
        elif self.ip_protocol() == 17:
            # UDP
            ret = 8
        elif self.ip_protocol() == 1:
            # ICMP
            ret = 4
        else:
            ret = None
        return ret

    def proto_source_port(self):
        if self.ip_protocol() == 6 or self.ip_protocol() == 17:
            # TCP and UDP
            ret = self._proto_header[0]
        else:
            ret = None
        return ret

    def proto_destination_port(self):
        if self.ip_protocol() == 6 or self.ip_protocol() == 17:
            # TCP and UDP
            ret = self._proto_header[1]
        else:
            ret = None
        return ret

    def proto_data(self):
        if self.ip_protocol() == 6 or self.ip_protocol() == 17:
            # TCP and UDP
            ret = self._proto_data
        else:
            ret = None
        return ret

    def proto_data_length(self):
        if self.ip_protocol() == 6 or self.ip_protocol() == 17:
            # TCP and UDP
            ret = len(self._proto_data)
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
        self._net_connections = []
        self._incoming = None
        self._outgoing = None

        # Run the sniffer asynchroniously
        try:
            self._sniffer = PacketSniffer()
        except Exception as e:
            self._sniffer = None
        else:
            self._sniffer.start()

    def stop(self):
        if self._sniffer is not None:
            self._sniffer.stop()

    def get(self):
        return self._stats

    def update(self):
        if self._sniffer is None:
            return False

        # Get the processes net stats
        packet = self._sniffer.get()

        # Get the net connection status thanks to the PsUtil lib
        # This call consumes CPU
        if packet is not None:
            self._net_connections = psutil.net_connections()

        # Empty packets queue
        while packet is not None:
            # Get the PID of the process which use the packet
            packet_pid = self.pid(packet)
            # Add the stats to the queue
            if packet_pid is not None:
                if packet_pid not in self._stats:
                    self._stats[packet_pid] = {'bytes_recv': 0, 'bytes_sent': 0}
                if self.incoming():
                    self._stats[packet_pid]['bytes_recv'] += packet['size']
                elif self.outgoing():
                    self._stats[packet_pid]['bytes_sent'] += packet['size']
            # Next packet
            packet = self._sniffer.get()

        return True

    def pid(self, packet):
        """Try to find the relative process PID
        Also found if it is a incoming or outgoing packet"""
        self._incoming = None
        self._outgoing = None
        for p in self._net_connections:
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
            and raddr[0] == packet['source_addr'] \
            and laddr[0] == packet['destination_addr'] \
            and raddr[1] == packet['source_port'] \
            and laddr[1] == packet['destination_port']

    def _match_outgoing(self, packet, laddr, raddr):
        """Check if the local laddr and remote raddr tuples (address, port)
        match the IP source/destination outgoing packet"""
        return raddr != () \
            and laddr != () \
            and laddr[0] == packet['source_addr'] \
            and raddr[0] == packet['destination_addr'] \
            and laddr[1] == packet['source_port'] \
            and raddr[1] == packet['destination_port']


def exit_program(signal, frame):
    n.stop()
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_program)
    n = NetTopStats()
    while True:
        time.sleep(3)
        n.update()
        print('=' * 80)
        pprint.pprint(n.get())
