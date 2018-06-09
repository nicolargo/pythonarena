#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PsUtil bench
#
# 500 iters with PsUtil version 5.4.3
# Delta   : 0:00:09.013591 (for cmdline)
# Delta   : 0:00:06.832873 (for cpu_percent)
# Delta   : 0:00:00.671494 (for cpu_times)
# Delta   : 0:00:02.752303 (for memory_info)
# Delta   : ~0 (for memory_percent)
# Delta   : 0:00:01.582691 (for name)
# Delta   : 0:00:00.624670 (for nice)
# Delta   : 0:00:00.105949 (for pid)
# Delta   : 0:00:00.570437 (for ppid)
# Delta   : 0:00:00.264209 (for status)
# Delta   : 0:00:12.426514 (for username)
# Delta   : 0:00:00.138800 (for status)
# Delta   : 0:00:00.374208 (for num_threads)


import psutil
from datetime import datetime

nbiter = 500
attrs_list = ['cmdline', 'cpu_percent', 'cpu_times', 'memory_info',
              'memory_percent', 'name', 'nice', 'pid', 'ppid',
              'status', 'username', 'status', 'num_threads']


def main(attrs):
    # PsUtil 5.3 or higher
    # If attrs is specified Process.as_dict() is called internally and the
    # resulting dict is stored as a info attribute which is attached to the
    # returned Process instances. If attrs is an empty list it will retrieve
    # all process info (slow).
    [proc.info for proc in psutil.process_iter(attrs=attrs, ad_value=None)]


if __name__ == '__main__':
    print('{} iters with PsUtil version {}'.format(nbiter,
                                                   psutil.__version__))

    last = None
    for i in range(0, len(attrs_list)):
        attrs = attrs_list[0:i+1]
        # print(attrs)
        start = datetime.now()
        for t in range(1, nbiter):
            main(attrs)
        duration = datetime.now() - start
        # print("Duration: {}".format(duration))
        if last is None:
            delta = duration
        else:
            delta = duration - last
        print("Delta   : {} (for {})".format(delta, attrs_list[i]))
        last = duration
