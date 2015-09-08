#!/usr/bin/env python
#
# Read TM raw files
#
#--------------------------
#

from __future__ import generators

__appname__ = 'pytm'
__version__ = "0.1"
__author__ = "Nicolas Hennion"
__licence__ = "LGPL"

# Libs
#=====

import sys
import getopt
import struct
import binascii
import re
import locale
import gettext
locale.setlocale(locale.LC_ALL, '')
gettext.install(__appname__)


# Classes
#========

class tmpacket(object):
    '''
    An ESA TM packet object (ESA PSS-04-106 Issue 1)
    '''

    __VN_MASK = 0xC000           # First 2 bits
    __PID_MASK = 0x07FF          # Last 11 bits
    __SEGMENTATION_MASK = 0xC000 # First 2 bits

    def read(self, buffer, seek):
        '''
        Read a TM packet in the buffer at the position seek
        Return position of the end of the packet
        '''
        
        # Header (6 bytes)
        header = buffer[seek:seek+6]
        packetidentification = int((header[0:2]).encode('hex'), 16)        
        self.vn = self.__VN_MASK & packetidentification
        if (self.vn != 0x8000):
            # Packet should start with 100 (bin) = 0x8000 (hex)
            print(_("Not a valid ESA TM packet"))
            sys.exit(2)
        self.pid = self.__PID_MASK & packetidentification
        self.segmentation = bin(self.__SEGMENTATION_MASK & int(header[2:4].encode('hex'), 16))[2:4]
        self.datalength = int(header[4:6].encode('hex'), 16)
        
        # Read packet data
        self.data = buffer[seek+6:seek+7+self.datalength]

        # Return position of the next packet
        return seek + 7 + self.datalength


    def __str__(self):
        '''
        How to print a TM packet
        '''
        buftohex = lambda x:" ".join([hex(ord(c))[2:].zfill(2) for c in x])        
        
        if (self.segmentation == "01"):
            segmentation_info = "First segment"
        elif (self.segmentation == "00"):
            segmentation_info = "Continuation segment"
        elif (self.segmentation == "10"):
            segmentation_info = "Last segment"
        elif (self.segmentation == "11"):
            segmentation_info = "Unsegmented"
        
        return "pid=%s\nsegmentation=%s (%s)\ndatalength=%s\n%s" % \
                (str(self.pid), \
                 str(self.segmentation), segmentation_info, \
                 str(self.datalength), \
                 re.sub("(.{63})", "\\1\n", buftohex(self.data), re.DOTALL))
    

class rawtmpacket(object):
    '''
    A RAW TM packet object
    8 byte (board date) + ESA TM packet
    '''

    def getDate(self, buffer, format = "%s/%s/%s %s:%s:%s:%s-%s"):
        '''
        Return the date containing in the buffer (8 bytes)
        or None if error
        '''
        if (len(buffer) != 8): return None
        day = str(int(hex(ord(buffer[0])),16))
        month = str(int(hex(ord(buffer[1])),16))  
        year = str(int(hex(ord(buffer[2])),16))
        hour = str(int(hex(ord(buffer[3])),16))
        minute = str(int(hex(ord(buffer[4])),16))
        second = str(int(hex(ord(buffer[5])),16))
        secondhundredth = str(int(hex(ord(buffer[6])),16))
        secondthousandth = str(int(hex(ord(buffer[7])),16))
        return format % \
                (day,month,year, \
                 hour,minute,second, \
                 secondhundredth,secondthousandth)


    def read(self, buffer, seek):
        '''
        Read a TM packet in the buffer at the position seek
        Return the position of the next packet
        '''
        
        # Read the date (8 bytes)
        self.boarddate = self.getDate(buffer[seek:seek+8])

        # Read the TM packet
        self.tmpacket = tmpacket()
        pos = self.tmpacket.read(buffer, seek+8)

        # Return position of the next packet
        return pos


    def __str__(self):
        '''
        How to print a RAW TM packet
        '''
        return "Date=%s\n%s" % ( self.boarddate, str(self.tmpacket))
        

class rawtmarchive(object):
    '''
    A RAW TM archive object
    '''

    def __init__(self):            
        self.rawtmlist = []

                    
    def readfile(self, filename):
        '''
        Read a TM file and put it in the rawtmlist
        '''
        try:
            with open(filename, 'rb') as f: pass
        except IOError as e:
            print(_("File %s is not readable") % filename)
            return False
            
        with open(filename, 'rb') as f:
            buffer = f.read()
        
        pos = 0
        while (pos < len(buffer)):
            rawpacket = rawtmpacket()
            pos = rawpacket.read(buffer, pos)
            #~ print "%s\n" % rawpacket
            self.rawtmlist.append(rawpacket)            

        return True

    def printall(self, pid = None):
        '''
        Print all the archive on STDOUT
        '''
        for t in self.rawtmlist:
            print t
            print("\n")

# Function

def printSyntax():
    pass
    

def printVersion():
    pass
    

def main():
    # Init variables
    filename = ''
    
    # Manage args
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
                                   "hvf:",
                                   ["help", "version", "file"])
    except getopt.GetoptError as err:
        # Print help information and exit:
        print(str(err))
        printSyntax()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-v", "--version"):
            printVersion()
            sys.exit(0)
        elif opt in ("-f", "--file"):
            try:
                arg
            except:
                print(_("Error: enter the TM file path"))
                sys.exit(2)
            filename = arg
        else:
            printSyntax()
            sys.exit(2)
            
    # Control args
    if (filename == ''):
        print(_("Error: -f <Tm file path> is mandatory"))
        sys.exit(2)        
    
    # Run
    tm = rawtmarchive()
    tm.readfile(filename) # '../../../../data/PW7_TM/PW7_2012_05_23_01_NRM.TLM'
    tm.printall()
    
    
# Main
#=====

if __name__ == "__main__":
    main()

# End
#====
