#!/usr/bin/env python

##############################################################
#	Project		: MULTI-PROJECT SCC
#	Module		: TMANA
#	Author		: VKO
#	File		: TMANA.py
#	Version		: see VERSION variable
#	Creation Date   : July 2012
#-------------------------------------------------------------
#
#	Copyright Thales Alenia Space 2012
#	All rights reserved
#
###############################################################
#
# Purpose :  Read TLM file, and display file analyse 
#
###############################################################
#
# Modifications :
#
# VKO : 26/07/2012 : V1.00 : iinitial version
#
###############################################################

from __future__ import generators


import string, sys, os
VERSION = "1.00"
PID_MASK = "07FF"
COMMENT = "#"
VERSION = "1.00"
#========================================================
# Define here TmAna conctant
# definir les constantes de TMANA ici
#========================================================
TrameLg = 1032 # lg totale en octets
DateLg = 8 # lg en octet
DateFormat = "FR_CAD" # valeurs acceptee : "FR_CAD"
DatePos = 0 # position 1 octet date dans la trame

class SCCpacket :
    """ Manage a packet """
    def init(self):
        """ define packet structure """
        self.date=""
        self.head=""
        self.pid=""
        self.lg=""
        self.ilg=""
        self.data=""

    def get_packet(self):
        """ return orininal packet """
        s=self.date[0:8]+self.head[0:6]+self.data
        return s
    
    def extract_packet(self, buf, skip):
        """ extract a packet from buffer, return index of last char extracted """
        # date on 8 bytes
        self.date = buf[skip+0:skip+8]
        # packet header on 6 bytes
        self.head = buf[skip+8:skip+14]
        # from header extract  id and lg
        xpid = \
               self._get2CharHexa(self.head[0:1]) +\
               self._get2CharHexa(self.head[1:2])

        #~ print xpid
        #~ print PID_MASK
        #~ print self._mask(xpid,PID_MASK)
        #~ print

        self.pid = long("0x"+self._mask(xpid,PID_MASK),16)

#       xseqctrl = \
#               self._get2CharHexa(self.head[2:3]) +\
#               self._get2CharHexa(self.head[3:4])


        xlg  = "0x" +\
               self._get2CharHexa(self.head[4:5]) +\
               self._get2CharHexa(self.head[5:6])
        self.lg = self.head[4:6]
        self.ilg = int(xlg,16)

        #~ print "lg = %s" % self.lg
        #~ print "ilg = %s" % self.ilg

        # data
        self.data = buf[skip+14:skip+15+self.ilg]
        idx = skip + 8 + 6 + self.ilg
        return idx
    
    def _mask(self, svalue, smask):
        """ apply mask on value """
        lv = len(svalue)
        lm = len(smask)
        s=""
        if lv != lm :
            print "WARNING, bad lg for mask"
            #s=svalue
        else :
            for i in range(0,lv,2):
                xv = int("0x"+svalue[i]+svalue[i+1],16)
                xm = int("0x"+smask[i]+smask[i+1],16)
                c = chr(xv & xm)
                s = s + self._get2CharHexa(c)
        return s
        
    def trace(self, level=0):
        """ print packet information """
        print "date : "+ self._printDate(self.date)
        print "pid : " + str(self.pid)
        print "lg  : " + str(self.ilg)
        if level > 1 :
            print "dhead : "
            self._printbufferHexa(self.head,"")
        if level > 2 :
            print "\ndata : "
            self._printbufferHexa(self.data,"")

    def _get2CharHexa(self, c) :
        """ from char in parameter get string of hexadecimal value in 'HH' format"""
        xc = hex(ord(c))
        if len(xc) == 3 :
            xc = xc[:2] + "0" + xc[2:]
        xc = xc[2:]
        return xc

    def _getCharHexa(self, c) :
        """ from char in parameter get string of hexadecimal value in '0xHH' format"""
        xc = hex(ord(c))
        if len(xc) == 3 :
            xc = xc[:2] + "0" + xc[2:]
        return xc
    
    def _printDate(self, date):
        """ from packet date get string in 'dd/mm/yy hh:mn:ss-mili' format """
        d = str(int(hex(ord(date[0])),16))
        m = str(int(hex(ord(date[1])),16))
        y = str(int(hex(ord(date[2])),16))
        h = str(int(hex(ord(date[3])),16))
        n = str(int(hex(ord(date[4])),16))
        s = str(int(hex(ord(date[5])),16))
        l1 = str(int(hex(ord(date[6])),16))
        l2 = str(int(hex(ord(date[7])),16))
        s = d+"/"+m+"/"+y+" "+h+":"+n+":"+s+":"+l1+"-"+l2
        return s
    
    def _printbufferHexa(self, buf, file_out) :
        """ print buffer in hexadecimal representation """
        lg = len(buf)
        j=1
        head1 = "00 :"
        line1 = ""
        line2 = ""
        fd_out = self._openAppendWrite(file_out)
        for i in range(lg) :
            c=buf[i:i+1]
            line1 = line1 + " " + self._getCharHexa(c)
            line2 = line2 + str(c)
            if j >= 10 :
                if fd_out != "" :
                    fd_out.write(line1)
                else :
                    #print head1 + line1 + "    " + line2
                    print head1 + line1
                j = 1
                head1 = str(i+1) + " :"
                line1 = ""
                line2 = ""
            else :
                j+=1
        cpl = ""
        while j <= 10 :
            cpl = cpl + " ...."
            j+=1
        if fd_out != "" :
            fd_out.write(line1)
        else :
            print head1 + line1 + cpl #+ "    " + line2
        if fd_out != "" :
            fd_out.close()
        
    def _openAppendWrite(self, filename):
        """ open file in append mode """
        if filename != "" :
            try :
                f=open(filename, "a+")
            except (IOError, os.error), why:
                    print " OPEN_ERROR " + filename + " : " + str(why)
        else :
            f = ""
        return f

#==========================================================================
class TMANA_F :
    """ Provide analyze of file """

    def __init__(self) :
        """ initialise instance """
        self.lst_packet=[]
        
    def applyFilter(self, file_in, way, file_out) :
        """ filter computation """
        stat = 0
        strnbremoved = 0
        if os.path.isfile(file_in) :
            try :
                fd_in = open(file_in, "rb")
                buf = fd_in.read()
            except (IOError, os.error), why:
                raise "AppliError", " OPEN_ERROR " + file_in + " : " + str(why)
            except :
                stat = 1
                raise "AppliError", " OPEN_ERROR " + file_in
            try :
                fd_in.close()
            except :
                print "error on " + file_in + " closure"
                pass

            if way == "T0" or way == "T1" or way == "T2" or way == "T3" or way == "T4" :
                if way == "T0" :
                    level = 0
                elif way == "T1" :
                    level = 1
                elif way == "T2" :
                    level = 2
                elif way == "T3" :
                    level = 3
                elif way == "T4" :
                    level = 4
                self._setPacketList(buf)
                self.ExaminePacketList(level)
            else :
                stat = 3

        else :
            stat = 2
        return stat, strnbremoved
    
    def _setPacketList(self, buf):
        """ translate input buffer in list of packet objects """
        lgbuf=len(buf)
        idx = -1
        self.lst_packet=[]
        while  idx+2 < lgbuf :
            item = SCCpacket()
            idx = item.extract_packet(buf, idx+1)
            self.lst_packet.append(item)
            
    def writePacketList(self, filterlist, file_out):
        """ write on output packets from list """
        cpt = 0
        fd_out = self.openWrite(file_out)
        for item in self.lst_packet :
            if item.pid not in filterlist : 
                s=item.get_packet()
                #print "trace : keep " + str(item.pid)
                if fd_out != "" :
                    fd_out.write(s)
                else :
                    print s
            else :
                cpt += 1
                #print "trace : remove " + str(item.pid)
        
        if fd_out != "" :
            fd_out.close()
        return str(cpt)
                
    def ExaminePacketList(self, level):
        """ trace packet list """
        if level == 1 :
            self.countPid()
        if level > 1 :
            for item in self.lst_packet :
                item.trace(level-1)
        print str(len(self.lst_packet)) + " packets"

    def countPid(self):
        dico = {}
        for item in self.lst_packet :
            pid = item.pid
            if dico.has_key(pid) :
                nb = dico[pid]
            else :
                nb = 0
            nb += 1
            dico[pid] = nb
        list = dico.keys()
        list.sort()
        #print list
        for k in list :
            print str(dico[k]) + " instance(s) of pid " + str(k)
            
    def openWrite(self, filename):
        """ open file in binary write mode and return file descritor"""
        if filename != "" :
            try :
                f=open(filename, "wb+")
            except (IOError, os.error), why:
                    print " OPEN_ERROR " + filename + " : " + str(why)
        else :
            f = ""
        return f

    
    def analyseLine(self, line, currentSection, outDico) :
        """ determine if line is section begining """
        line = self.removeDiese(line)
        idx1 = line.find("[")
        idx2 = line.find("]")
        if idx1 != -1 and idx2 != -1 :
            currentSection = line[idx1+1:idx2]
        else :
            self.analyseVariable(line,currentSection, outDico)
        return currentSection

    def analyseVariable(self, line, currentSection, outDico):
        """ add value for section"""
        listKnownKeys = []
                
        if outDico.has_key(currentSection):
            varList = outDico[currentSection]
        else :
            varList = []
        splitten = line.split(None, 1)
        if len(splitten) > 0 :
            Key = splitten[0]
            if len(splitten) > 1 :
                Value = splitten[1]
            else :
                Value = ""
                splitten.append(Value)
#            print Key + " ==> " + Value
            varList.append(splitten)
            outDico[currentSection] = varList


    def removeDiese(self, line):
        """ remove comment in line """
        idx = line.find(COMMENT)
        if idx != -1 :
            newLine = line[:idx]
        else :
            newLine = line
        return newLine.strip()

class TMANAmain:
    """ Entry class for manage Telemetry A """
    def __init__(self):
        """ attribute initialisation """
        self.TrameLg = TrameLg
        self.DateLg = DateLg
        self.DateFormat = DateFormat
        self.DatePos = DatePos
        self.input = ""
        self.output  = ""
        self.way = "T0"

    def usage(self, outfile) :
        outfile.write("""
      Read TM file and Write TM file analyze
      Usage:
      %s
          input_file [way] [output_file]
      or
          option
    
      input_file  : original file
      way : "T0" display buffer summary
            "T1" display buffer analyse
            "T2" display buffer analyse with packet
            "T3" display buffer analyse with paket and head in hexadecimal code
            "T4" display buffer analyse with paket and hexadecimal code
      output_file : result file (optional)
      option :
      -h : print this message and exit
      -v : print version and exit
    """ % sys.argv[0])

    def chekArg(self):
        """ check correctness of the command """
        
        stat = 0
        nbArg = len(sys.argv)     # number of arguments (the first argument corresponds to the command)


        if (nbArg > 1):
            if (sys.argv[1] == '-h'):
                self.usage(sys.stdout)
                sys.exit(0)

            if (sys.argv[1] == '-v'):
                print VERSION
                sys.exit(0)

        if (nbArg == 1):
            self.usage(sys.stdout)
            sys.exit(0)

        if (nbArg <= 1):
            print >> sys.stderr,'ERROR : argument missing'
            self.usage(sys.stderr)
            sys.exit(1)
        if (nbArg > 4):
            print >> sys.stderr,'ERROR : too much arguments'
            self.usage(sys.stderr)
            sys.exit(1)

        self.input   = sys.argv[1]
        if (nbArg > 2):
            self.way   = sys.argv[2]
        if nbArg == 4 :
            self.output = sys.argv[3]

        return stat

    def process(self):
        """ process command """
        inf = 0
        converter = TMANA_F()
        inf, nb = converter.applyFilter( self.input, self.way, self.output)
        if inf == 1 :
            print "Error occured"
        elif inf == 2 :
            print self.input + " file not found"
        elif inf == 3 :
            print "Error : wrong a"


    def main(self) :
        """
        entry for TeleMetry Analyzer
        check arguments then execute analyze
        """
        ok = self.chekArg()
        if ok == 0 :
            self.process()


#---------------------------------------------------------
# Used in stand alone ONLY
#=========================================================
if __name__ == "__main__":
    TMANA = TMANAmain()
    TMANA.main()
