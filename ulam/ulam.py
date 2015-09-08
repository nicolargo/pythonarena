#!/usr/bin/env python

from __future__ import generators

__appname__ = 'ulam'
__version__ = "0.1"
__author__ = "Nicolas Hennion <nicolas@nicolargo.com>"
__licence__ = "GPL version 3"

from pylab import plot, axis,savefig, show, title

# plot([5,10], [15, 20])
# title("Ulam")
# savefig("ulam.png")
# show()

# Functions
#==========

def isprime(n):
    '''
    Return True if n is a prime number
    False if not
    '''

    if (not n % 2):
        return False
    i = 3
    while (i < n):
        if ((n / float(i)).is_integer()):
            return False
        i += 1
    return True

# Main
#=====

if __name__ == "__main__":

    # isprime(5)
    # isprime(6)
    # exit()

    primelist = []
    # TODO: Factorised in Python way
    for i in xrange(0, 1000):
        if (isprime(i)):
            primelist.append(i)
    print primelist
    print len(primelist)

