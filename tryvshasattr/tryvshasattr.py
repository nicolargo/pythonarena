# -*- coding: utf-8 -*-
#
# Nicolargo (12/2016)
#
# try_ok  : 0.0228261947632
# in_ok   : 0.0185971260071
# try_nok : 0.117195129395
# in_nok  : 0.0177400112152


import timeit

d = {'a': 1, 'b': 2, 'c': 3}

def try_ok():
    try:
        d['a']
    except KeyError:
        pass

def try_nok():
    try:
        d['d']
    except KeyError:
        pass

def in_ok():
    if 'a' not in d:
        pass

def in_nok():
    if 'd' not in d:
        pass

if __name__ == '__main__':
    t = timeit.Timer(lambda: try_ok())
    print('{:8}: {}'.format('try_ok', t.timeit(number=100000)))
    t = timeit.Timer(lambda: in_ok())
    print('{:8}: {}'.format('in_ok', t.timeit(number=100000)))
    t = timeit.Timer(lambda: try_nok())
    print('{:8}: {}'.format('try_nok', t.timeit(number=100000)))
    t = timeit.Timer(lambda: in_nok())
    print('{:8}: {}'.format('in_nok', t.timeit(number=100000)))
