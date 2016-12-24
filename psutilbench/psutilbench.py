#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PsUtil bench
#
# ===================================================================
# 500 iters with PsUtil 5.0.1:
# real	0m10.761s
# user	0m8.324s
# sys	0m2.412s
#
# 500 iters with PsUtil 5.0.0:
# real	0m10.708s
# user	0m8.200s
# sys	0m2.484s
#
# 500 iters with PsUtil 4.3.1:
# real	0m16.375s
# user	0m10.752s
# sys	0m5.544s
# ===================================================================
# 500 iters with PsUtil 5.0.0:
# real	0m18.176s
# user	0m14.264s
# sys	0m3.876s
#
# 500 iters with PsUtil 4.3.1:
# real	0m30.422s
# user	0m19.792s
# sys	0m10.520s
# ===================================================================


import psutil

nbiter = 500


def main():
    for proc in psutil.process_iter():
        proc.as_dict(
            attrs=['name', 'cpu_times', 'create_time',
                   'ppid', 'status', 'terminal'], ad_value='')


if __name__ == '__main__':
    print('PsUtil version {}'.format(psutil.__version__))
    for i in range(1, nbiter):
        main()
