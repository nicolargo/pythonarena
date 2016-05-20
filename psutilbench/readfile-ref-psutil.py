#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil

nbiter = 20000

def main():
    return psutil.cpu_times()

if __name__ == '__main__':
    for i in range(1, nbiter):
        main()
