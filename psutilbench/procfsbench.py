#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Procfs bench
# https://github.com/pmuller/procfs
#
# Nicolargo (2015)
# MIT Licence

from procfs import Proc

nbiter = 500

def main():
    proc = Proc()
    for p in proc.processes:
        mem = p.status

if __name__ == '__main__':
    for i in range(1, nbiter):
        main()