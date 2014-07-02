#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

nbiter = 20000

def main():    
    f = open('/proc/stat', 'r')
    try:
        values = f.readline().split()        
    finally:
        f.close()
    fields = ['user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq', 'steal', 'guest',
     'guest_nice']
    d = namedtuple('cpu', fields)
    return d(*values[1:])

if __name__ == '__main__':    
    for i in range(1, nbiter):
        main()
