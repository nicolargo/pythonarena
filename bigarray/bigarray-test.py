#!/usr/bin/env python
#
# Test big array computing
#
#--------------------------
#
# Result on my Ubuntu Linux machine
# Core i5 / 8 Go RAM
#
# 50 TM / 360 days
#   min process 	Result: 1.54 seconds
#   max process 	Result: 1.55 seconds
#   mean process 	Result: 2.86 seconds
#   cumul process 	Result: 0.99 seconds
#   integ process 	Result: 20.64 seconds
#   diff process 	Result: 33.09 seconds
#


from __future__ import generators

__appname__ = 'bigarray-test'
__version__ = "0.1"
__author__ = "Nicolas Hennion <nicolas@nicolargo.com>"
__licence__ = "LGPL"


# Libs
#=====

import sys
import timeit
# To be installed on the system
from numpy import *
from scipy import integrate

# Classes
#========

class bigarray:
    """
    Define a big array
    Fct use Numpy http://www.scipy.org/Numpy_Example_List
    """
    
    def __init__(self, s):
        """
        s = size
        """
        self.array = random.randint(360, size=(1, s))[0]

    def size(self, start = 0, end = None):
        return self.array[start:end].size

    def min(self, start = 0, end = None):
        return self.array[start:end].min()

    def max(self, start = 0, end = None):
        return self.array[start:end].max()

    def mean(self, start = 0, end = None):
        return average(self.array[start:end])

    def cumul(self, start = 0, end = None):
        return self.array[start:end].sum()

    def integ(self, start = 0, end = None):
        # Integrate using the composite trapezoidal rule
        return integrate.trapz(self.array[start:end])
        # Alternative / Slower: Integrate using the composite Simpson s rule
        #~ return integrate.simps(self.array[start:end])

    def diff(self, start = 0, end = None):
        # Return the gradient of the array.
        # The gradient is computed using central differences in the interior 
        # and first differences at the boundaries.
        return gradient(self.array[start:end])

# Functions
#==========

def bench_min():
    ba.min()

def bench_max():
    ba.max()

def bench_mean():
    ba.mean()

def bench_cumul():
    ba.cumul()    
    
def bench_integ():
    ba.integ()        

def bench_diff():
    ba.diff()        


# Main
#=====

if __name__ == "__main__":
    # Init environment
    nbday = 360
    nbtm = 50    
    tobebench = ["min", "max", "mean", "cumul", "integ", "diff" ]
    
    # Init the table
    ba = bigarray(nbday * 24 * 3600)   
    
    # Start the bench
    print "%d TM / %d days" % (nbtm, nbday)
    for b in tobebench: 
        print "%8s process" % b,
        sys.stdout.flush()
        setup = "from __main__ import bench_%s" % b
        process = "bench_%s()" % b
        t = timeit.Timer(process, setup)
        print "\tResult: %.2f seconds" % t.timeit(nbtm)    
    
    # Exit
    sys.exit(0)

# End
#====
