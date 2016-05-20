# -*- coding: utf-8 -*-
#
# Alternative to Numpy vstack
# Why: because vstack copy the whole arrays
# Nicolargo (11/2015)
#

A_SIZE = 80000

# from memory_profiler import profile
import numpy as np
import os
import psutil

def get_rss():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss

# @profile
def test_vstack(a, b):
    return np.vstack((a, b))

# @profile
def test_vstack_lowmemory(a, b, pos=0):
    a[pos] = b

if __name__ == '__main__':
    rss1 = get_rss()
    a = np.random.rand(1, A_SIZE)[0]
    b = np.random.rand(1, A_SIZE)[0]
    c = test_vstack(a, b)
    print("vstack memory consumption      = %d" % (get_rss() - rss1))
    del a, b, c

    rss1 = get_rss()
    c = np.empty([2, A_SIZE])
    test_vstack_lowmemory(c, np.random.rand(1, A_SIZE)[0], pos=0)
    test_vstack_lowmemory(c, np.random.rand(1, A_SIZE)[0], pos=1)
    print("alternative memory consumption = %d" % (get_rss() - rss1))
    del c
