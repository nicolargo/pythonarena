#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Timestamp compression test bed
#
# Source: http://www.vldb.org/pvldb/vol8/p1816-teller.pdf
# Chapter: 4.1.1
#

import sys
import array

def show_sizeof(x, level=0):
    print "\t" * level, x.__class__, sys.getsizeof(x)
    # if hasattr(x, '__iter__'):
    #     if hasattr(x, 'items'):
    #         for xx in x.items():
    #             show_sizeof(xx, level + 1)
    #     else:
    #         for xx in x:
    #             show_sizeof(xx, level + 1)

def main():
    # raw = [0, 0, 0, 0, 0, 1, 2, 3, 5, 5, 5]
    raw = [0.0] * 100 + [3.0, 3.0, 3.0, 3.8, 9.55, 50.0, 100.0, 100.0, 100.0, 100.0, 9.0, 3.0, 3.0]

    # COMPRESSION
    # Raw        [0, 0, 0, 0, 0, 1, 2, 3, 5, 5, 5] (List)
    # Optimize duplicated values in a array of signed short int
    # Cast float to int (float * 100) / Precision 0.01
    # Compressed [0, -4, 10, 20, 30, 50, -2] (Array)
    #############

    compressed = array.array('h')
    v_cpt = 0
    v_old = None
    for v in raw:
        v_new = int(v * 100.0)
        if v_new == v_old:
            v_cpt += 1
            if v_cpt == 1:
                compressed.append(-v_cpt)
            else:
                try:
                    compressed[len(compressed) - 1] = -v_cpt
                except OverflowError:
                    # Can not store more than 32676 duplicated values
                    compressed[len(compressed) - 1] = -v_cpt + 1
                    compressed.append(v_old)
                    v_cpt = 0
        else:
            compressed.append(v_new)
            v_cpt = 0
        v_old = v_new
    print(compressed)

    # DECOMPRESSION
    # Compressed   [0, -4, 10, 20, 30, 50, -2] (Array)
    # Rebuild duplicated values
    # Decompressed [0, 0, 0, 0, 0, 1, 2, 3, 5, 5, 5] (List)
    ###############

    decompressed = []
    v_old = None
    for v in compressed:
        v_new = float(v / 100.0)
        if v < 0:
            decompressed += [v_old] * -v
        else:
            decompressed.append(v_new)
            v_old = v_new

    # print(raw)
    # show_sizeof(raw)
    # print(compressed)
    # show_sizeof(compressed)
    # print(delta)
    # print(decompressed)

    if raw == decompressed:
        rate = 100 - (sys.getsizeof(compressed) * 100.0 / sys.getsizeof(raw))
        print('OK. Compression rate is %.2f%%' % rate)
    else:
        print('ERROR')

if __name__ == '__main__':
    main()
