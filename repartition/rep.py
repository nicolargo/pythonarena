#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rep.py
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
#  


def main():
    freq = 3600/450
    for i in range(3600):
        if ((i % freq) == 1):
            print "Tick on %d - %d" % (i, i % freq)
    return 0

if __name__ == '__main__':
    main()

