# -*- coding: utf-8 -*-
#
# POC for Wifi
# Nicolargo (10/2016)
#

import wifi

w = wifi.Cell.all('wlp2s0')

for c in w:
    print('{} ({}) {}'.format(c.ssid,
                              c.quality,
                              c.encryption_type if c.encrypted else 'open'))
