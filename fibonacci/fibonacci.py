#!/usr/bin/env python

__appname__ = 'fibonacci'
__version__ = "0.1"
__author__ = "Nicolas Hennion <nicolas@nicolargo.com>"
__licence__ = "LGPL"


class fibonnacci(object):

    fibonacci_table = []

    def __init__(self):
        self.fibonacci_table.append(0)
        self.fibonacci_table.append(1)

    def compute(self, n):
        try:
            ret = self.fibonacci_table[n]
        except:
            ret = self.compute(n - 2) + self.compute(n - 1)
            self.fibonacci_table.append(ret)
        return ret


def main():
    f = fibonnacci()
    for i in range(2, 800):
        print("%s" % f.compute(i))


if __name__ == '__main__':
    main()
