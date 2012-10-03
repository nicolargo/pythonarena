#!/usr/bin/env python
#
# Test chart generation PyGal and big table 
#

from __future__ import generators

__appname__ = 'bigchart'
__version__ = "0.1"
__author__ = "Nicolas Hennion <nicolas@nicolargo.com>"
__licence__ = "LGPL"

# Libs
#=====

import sys
import timeit
from time import time
import random
import pygal

# Main
#=====

if __name__ == "__main__":

   # Global variable
   _DATA_SIZE = 365 * 24 * 60 * 60
   _DATA_SAMPLE = 51
   _CHART_FILE = 'chart'

   # Init the table
   print "Init the data table (size %d)" % _DATA_SIZE
   data = list(xrange(_DATA_SIZE))
   chart = pygal.Line(title = "Test of the Pygal API")

   print "Let's start..."
   t0 = time()

   # Sample
   print "Sample data (%s to %s)" % (_DATA_SIZE, _DATA_SAMPLE)
   sample = []
   sample_number = _DATA_SIZE / _DATA_SAMPLE
   for i in range(_DATA_SAMPLE):
      sample_sub = data[i*sample_number:(i+1)*sample_number]
      sample_average = reduce(lambda x,y: x+y, sample_sub, 0) / sample_number
      sample.append(sample_average)

   # Generate the chart
   print "Add sample data to the chart"
   chart.add('Data', sample)
   
   tf = round(time() - t0, 3)
   print "Time elapsed: %.2f" % tf

   # Export the chart to SVG
   print "Export the chart to SVG file (%s.svg)" % _CHART_FILE
   chart.render_to_file(_CHART_FILE+".svg")

   tf = round(time() - t0, 3)
   print "Time elapsed: %.2f" % tf
   
   # Export the chart to PNG
   print "Export the chart to SVG file (%s.png)" % _CHART_FILE
   chart.render_to_png(_CHART_FILE+".png")

   tf = round(time() - t0, 3)
   print "Time elapsed: %.2f" % tf
   
   # Exit
   sys.exit(0)

