#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Timestamp compression test bed
#
# Source: http://www.vldb.org/pvldb/vol8/p1816-teller.pdf
# Chapter: 4.1.1
#

from memory_profiler import profile
import sys
from datetime import datetime

def show_sizeof(x, level=0):
    print "\t" * level, x.__class__, sys.getsizeof(x)
    # if hasattr(x, '__iter__'):
    #     if hasattr(x, 'items'):
    #         for xx in x.items():
    #             show_sizeof(xx, level + 1)
    #     else:
    #         for xx in x:
    #             show_sizeof(xx, level + 1)

# @profile
def main():
    without_compression = []
    for i in xrange(0, 1000):
        without_compression.append(datetime.now())
    show_sizeof(without_compression)

    with_compression = []
    t_previous = None
    for i in xrange(0, 1000):
        t_now = datetime.now()
        if with_compression == []:
            with_compression.append(t_now)
        else:
            with_compression.append((t_now - t_previous).total_seconds())
        t_previous = t_now
    show_sizeof(with_compression)

if __name__ == '__main__':
    main()
