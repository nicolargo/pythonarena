#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Glances Processes bench
#
# ===================================================================
# 500 iters with PsUtil version 5.4.2
# Pure PsUtil
# real	0m27.454s
# user	0m20.100s
# sys	0m7.228s
#
# 500 iters with PsUtil version 5.4.2
# Glances version 2.11.1
# real	0m44.059s
# user	0m32.728s
# sys	0m11.216s

# ===================================================================

import psutil
from glances.processes import GlancesProcesses
from glances import __version__

nbiter = 10
attrs_list = ['cmdline', 'cpu_percent', 'cpu_times',
              'io_counters', 'memory_info',
              'memory_percent', 'name', 'nice',
              'pid', 'ppid', 'status', 'username']


# def bench():
#     print("Pure PsUtil")
#     for i in range(1, nbiter):
#         l = [proc.info for proc in psutil.process_iter(attrs=attrs_list, ad_value='')]
#     return l


def bench():
    print("Glances version {}".format(__version__))
    p = GlancesProcesses()
    for i in range(1, nbiter):
        p.update()
        l = p.getlist()
    return l


if __name__ == '__main__':
    print('{} iters with PsUtil version {}'.format(nbiter,
                                                   psutil.__version__))
    l = bench()
    print(len(l))
    for p in l:
        if p['pid'] == 1:
            print(p)
