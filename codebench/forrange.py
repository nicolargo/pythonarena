#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Bench
#  
#  Copyright 2013 nicolargo <nicolas@nicolargo.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

from time import time

list = "A" * 10000000

t0 = time()
for x in range(0, len((list))):
    list[x]
t1 = round(time() - t0, 3)

t0 = time()    
for x in list:
    x
t2 = round(time() - t0, 3)

print "Time for x in range...: %.2f" % t1
print "Time for x in list... : %.2f" % t2
