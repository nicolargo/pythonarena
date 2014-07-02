#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

nbiter = 10000

def main():
    with open('/proc/stat', 'r') as f:
        values = f.readline().split()        
    fields = ['user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq', 'steal', 'guest',
     'guest_nice']
    return dict(zip(fields, values[1:]))

if __name__ == '__main__':
    for i in range(1, nbiter):
        main()
