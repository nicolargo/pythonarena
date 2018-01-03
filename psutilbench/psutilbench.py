#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PsUtil bench
#
# ===================================================================
# 500 iters with PsUtil version 5.4.2
# real	0m10.578s
# user	0m8.104s
# sys	0m2.448s
#
# 500 iters with PsUtil version 5.0.1
# real	0m10.761s
# user	0m8.324s
# sys	0m2.412s
#
# 500 iters with PsUtil version 5.0.0
# real	0m10.708s
# user	0m8.200s
# sys	0m2.484s
#
# 500 iters with PsUtil version 4.3.:
# real	0m16.375s
# user	0m10.752s
# sys	0m5.544s
# ===================================================================


import psutil

nbiter = 500
attrs_list = ['name', 'cpu_times', 'create_time',
              'ppid', 'status', 'terminal']


def main():
    try:
        # PsUtil 5.3 or higher
        for proc in psutil.process_iter(attrs=attrs_list, ad_value=''):
            proc.info
        # Or ...
        # [proc.info for proc in psutil.process_iter(attrs=attrs_list, ad_value='')]
    except TypeError:
        for proc in psutil.process_iter():
            proc.as_dict(attrs=attrs_list, ad_value='')


if __name__ == '__main__':
    print('{} iters with PsUtil version {}'.format(nbiter,
                                                   psutil.__version__))
    for i in range(1, nbiter):
        main()
