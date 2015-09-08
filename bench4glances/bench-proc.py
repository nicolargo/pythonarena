#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import psutil
from time import time

cmdlines_cache = {}

def process_list_psutil():
    # pids = names = cmdlines = []
    pids = []
    names = []
    cmdlines = []
    for p in psutil.process_iter():
        pids.append(p.pid)
        names.append(p.name)
        try:
            cmdlines_cache[p.pid]
        except:
            cmdlines_cache[p.pid] = p.cmdline
        finally:
            cmdlines.append(cmdlines_cache[p.pid])

def process_list_homemade():
    """Bench to get process list"""
    pids = [int(x) for x in os.listdir('/proc') if x.isdigit()]
    try:
        names = [open(os.path.join('/proc', str(pid), 'stat'), 'rb').read().split(' ')[1].replace('(', '').replace(')', '') for pid in pids]
        cmdlines = [open(os.path.join('/proc', str(pid), 'cmdline'), 'rb').read().split('\x00') for pid in pids]
    except IOError as e:
        pass

class process_list_ng():

    def __init__(self):
        self.__update__()
        self.names = []
        self.cmdlines = []

    def __update__(self):
        self.pids = [int(x) for x in os.listdir('/proc') if x.isdigit()]


if __name__ == '__main__':
    n = 100
    pl = ["process_list_psutil", "process_list_homemade"]
    for p in pl:
        print("%d %s" % (n, p))
        t0 = time()
        for i in range(0, n):
            globals()[p]()
        print("\_ {}s".format(str(round(time() - t0, 3))))
