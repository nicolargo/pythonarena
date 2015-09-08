#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PsUtil 2.0 bench
#
# Test patch
#
# diff -r e3da966369df psutil/__init__.py
# --- a/psutil/__init__.py    Tue Mar 25 23:55:18 2014 +0100
# +++ b/psutil/__init__.py    Fri Mar 28 18:18:11 2014 +0100
# @@ -1289,12 +1289,7 @@
#              if proc is None:  # new process
#                  yield add(pid)
#              else:
# -                # use is_running() to check whether PID has been reused by
# -                # another process in which case yield a new Process instance
# -                if proc.is_running():
# -                    yield proc
# -                else:
# -                    yield add(pid)
# +                yield proc
#          except NoSuchProcess:
#              remove(pid)
#          except AccessDenied:
#

import psutil

nbiter = 500

def main():
    for proc in psutil.process_iter():
        cpu = proc.get_cpu_percent(interval=None)
        mem = proc.get_ext_memory_info().rss

if __name__ == '__main__':
    for i in range(1, nbiter):
        main()
