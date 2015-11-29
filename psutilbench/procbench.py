#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Proc bench
# https://pypi.python.org/pypi/proc
#
# Slower than PsUtil
# > time python procbench.py 
# real    0m19.769s
# user    0m17.587s
# sys 0m2.182s
# > time python psutilbench.py 
# real    0m12.478s
# user    0m7.764s
# sys 0m4.714s
#

from proc.core import find_processes

nbiter = 500

def main():
    for p in find_processes():
        pid = p.pid
        mem = p.rss

if __name__ == '__main__':
    for i in range(1, nbiter):
        main()
