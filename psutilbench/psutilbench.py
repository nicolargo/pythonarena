#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PsUtil bench
#

# 500 iters with PsUtil version 5.8.0
# Delta   : 0:00:12.783057 (for cmdline)
# Delta   : 0:00:06.264293 (for cpu_percent)
# Delta   : 0:00:00.841236 (for cpu_times)
# Delta   : 0:00:04.244486 (for memory_info)
# Delta   : 0:00:01.313005 (for memory_percent)
# Delta   : 0:00:02.632584 (for name)
# Delta   : -1 day, 23:59:58.992715 (for nice)
# Delta   : 0:00:00.484527 (for pid)
# Delta   : 0:00:00.016478 (for ppid)
# Delta   : 0:00:01.037471 (for status)
# Delta   : 0:00:10.766456 (for username)
# Delta   : -1 day, 23:59:59.781488 (for status)
# Delta   : 0:00:01.277902 (for num_threads)

#500 iters with PsUtil version 6.0.0
#Delta   : 0:00:03.115946 (for cmdline)
#Delta   : 0:00:02.705392 (for cpu_percent)
#Delta   : 0:00:00.455487 (for cpu_times)
#Delta   : 0:00:01.476142 (for memory_info)
#Delta   : 0:00:00.256081 (for memory_percent)
#Delta   : 0:00:01.535933 (for name)
#Delta   : 0:00:00.280973 (for nice)
#Delta   : 0:00:00.053392 (for pid)
#Delta   : 0:00:03.002009 (for ppid)
#Delta   : 0:00:00.132980 (for status)
#Delta   : 0:00:03.550328 (for username)
#Delta   : -1 day, 23:59:59.945258 (for status)
#Delta   : 0:00:00.276642 (for num_threads)


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
