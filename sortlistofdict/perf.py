# -*- coding: utf-8 -*-

import timeit
from random import randint
from operator import itemgetter
import psutil

# Number of iterations
n = 3000

# Generate a list of dict for the bench
list_size = 10000
l = []
for i in range(list_size):
    l.append({'id': randint(1, list_size),
              'name': 'name' + str(randint(1, list_size))})

def perf_1():
    return sorted(l, key=lambda d: d['id'])

def perf_2():
    return sorted(l, key=itemgetter('id'))

if __name__ == '__main__':
    p = psutil.Process()
    print(p.cpu_times())
    print("sorted(l, key=lambda d: d['id']) => {} ".format(timeit.timeit("perf_1()",
                                                           setup="from __main__ import perf_1",
                                                           number=n)))
    print(p.cpu_times())
    print("sorted(l, key=itemgetter('id'))  => {} ".format(timeit.timeit("perf_1()",
                                                           setup="from __main__ import perf_1",
                                                           number=n)))
    print(p.cpu_times())
