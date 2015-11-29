#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PsUtil bench
#


import psutil

nbiter = 500

def main():
    for p in psutil.process_iter():
        cpu = p.cpu_percent(interval=None)
        mem = p.memory_info_ex().rss

if __name__ == '__main__':
    for i in range(1, nbiter):
        main()
