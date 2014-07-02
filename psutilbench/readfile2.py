#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

nbiter = 20000

def main():
    with open('/proc/stat', 'r') as f:
        values = f.readline().split()        
    fields = ['user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq', 'steal', 'guest',
     'guest_nice']
    d = dict(zip(fields, values[1:]))
    # The namedtuple conversion is the congestion point...
    return namedtuple('cpu', d.keys())(**d)

if __name__ == '__main__':
    for i in range(1, nbiter):
        main()
