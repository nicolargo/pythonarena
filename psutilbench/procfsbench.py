# Bench of the ProcFS lib
# https://github.com/pmuller/procfs
#
# Nicolargo (2015)
# MIT Licence


from procfs import Proc
import time

proc = Proc()

while True:
    for p in proc.processes:
        try:
            p.io
        except Exception as e:
            print "ERROR: %s" % e
        try:
            p.cmdline
            p.status
            p.stat
            p.statm
            p.smaps
        except Exception as e:
            print "ERROR: %s" % e
    time.sleep(3)
