#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# RRDTool test bed
#
# Note: sudo apt-get install python-rrdtool

import rrdtool
import time


def main():
    rrdtool.create('/tmp/example.rrd',
                   '--step', '1',
                   '--start', '0',
                   'DS:test:GAUGE:9:U:U',
                   'RRA:AVERAGE:0.5:1:60')

    for i in range(1, 60):
        v = 'N:%d' % i
        print(v)
        rrdtool.update('/tmp/example.rrd', v)
        time.sleep(1)

    rrdtool.graph('/tmp/example.png',
                  '--imgformat', 'PNG',
                  '--width', '540',
                  '--height', '100',
                  '--start', '0',
                  '--end', '-1',
                  'DEF:test1=/tmp/example.rrd:test:AVERAGE',
                  'AREA:test1#00FF00:Test1')

if __name__ == '__main__':
    main()
