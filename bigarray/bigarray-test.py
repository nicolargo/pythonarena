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
#     min process 	Result: 1.54 seconds
#     max process 	Result: 1.55 seconds
#    mean process 	Result: 2.88 seconds
#   cumul process 	Result: 1.00 seconds
#   smooth process 	Result: 144.07 seconds
#   integ process 	Result: 26.44 seconds
#    diff process 	Result: 32.92 seconds
#

from __future__ import generators

__appname__ = 'bigarray-test'
__version__ = "0.2"
__author__ = "Nicolas Hennion <nicolas@nicolargo.com>"
__licence__ = "LGPL"

# Libs
#=====

import sys
import timeit
from time import time
# To be installed on the system
import numpy
from scipy import integrate
try:
    import multiprocessing
    nbcore = multiprocessing.cpu_count()
except:
    pass

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
        self.array = numpy.random.randint(360, size=(1, s))[0]        

    def val(self, start = 0, end = None):
        '''
        Return the table or subtable
        '''
        return self.array[start:end]

    def size(self, start = 0, end = None):
        '''
        Return the table or subtable size
        '''
        return self.array[start:end].size

    def min(self, start = 0, end = None):
        '''
        Return the minimal value of the table or subtable size
        '''
        return self.array[start:end].min()

    def max(self, start = 0, end = None):
        '''
        Return the maximal value of the table or subtable size
        '''
        return self.array[start:end].max()

    def smooth(self, start = 0, end = None, window = 100):
        '''
        Return the moving average table of the table or subtable size
        '''
        tw = numpy.repeat(1.0, window) / window
        return numpy.convolve(self.array[start:end], tw)[window-1:-(window-1)]

    def mean(self, start = 0, end = None):
        '''
        Return the mean value of the table or subtable size
        '''        
        return numpy.average(self.array[start:end])

    def cumul(self, start = 0, end = None):
        '''
        Return the sum (cumul) value of the table or subtable size
        '''        
        return self.array[start:end].sum()

    def integ(self, start = 0, end = None):
        '''
        Return the integrate table of the table or subtable size
        '''
        # Integrate using the composite trapezoidal rule
        # return integrate.trapz(self.array[start:end]) 
        # Alternative mode precise but slower: Integrate using the composite Simpsons rule
        # return integrate.simps(self.array[start:end])
        # Cumulative integration using the composite trapezoidal rule
        return integrate.cumtrapz(self.array[start:end])

    def diff(self, start = 0, end = None):
        '''
        Return the differencial table of the table or subtable size
        '''
        # Return the gradient of the array.
        # The gradient is computed using central differences in the interior 
        # and first differences at the boundaries.
        return numpy.gradient(self.array[start:end])

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

def bench_smooth():
    ba.smooth()        
    
def bench_integ():
    ba.integ()        

def bench_diff():
    ba.diff()        


# Main
#=====

if __name__ == "__main__":
    # Init environment
    nbday = 365
    nbtm = 50    
    tobebench = ["min", "max", "mean", "cumul", "smooth", "integ", "diff" ]
    #~ tobebench = ["min", "max", "mean", "cumul" ]
            
    # Init the table
    ba = bigarray(nbday * 24 * 3600)   
    
    
    # Start the bench
    print "%d TM / %d days\n" % (nbtm, nbday)    
    print "Serial computation..." 
    t0 = time()     
    for b in tobebench: 
        print "%8s process" % b,
        sys.stdout.flush()
        setup = "from __main__ import bench_%s" % b
        process = "bench_%s()" % b
        t = timeit.Timer(process, setup)
        print "\rResult: %.2f seconds" % t.timeit(nbtm)        
    ts = round(time() - t0, 3) 
    print "Time elapsed in serial computation: %.2f\n" % ts

    # Multiprocessing
    print "Multiprocessing computation on a %d-core..." % nbcore
    t0 = time()     
    pool = multiprocessing.Pool(processes = nbcore)
    for i in range(nbtm):
        for p in tobebench:
            function = globals()["bench_" + p]
            pool.apply_async(function)
    pool.close()
    pool.join()
    tp = round(time() - t0, 3) 
    print "Time elapsed in multiprocessing computation: %.2f\n" % tp

    # Compare
    print "Speed-up: %sx \n" % round(ts/tp, 2) 
    
    # Exit
    sys.exit(0)

# End
#====
