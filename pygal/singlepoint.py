#!/usr/bin/env python
#
# Test Pygal wih single point
#

from __future__ import generators

__appname__ = 'singlepoint'
__version__ = "0.1"
__author__ = "Nicolas Hennion <nicolas@nicolargo.com>"
__licence__ = "LGPL"

# Libs
#=====

import pygal

# Main
#=====

if __name__ == "__main__":

    _CHART_FILE = "singlepoint"

    chart = pygal.XY(stroke=False)

    chart.title = "Test Pygal"

    chart.add('Test data', [(0.0, 20.0), (0.067, 140.0), (1.7, 140)])

    # Export the chart to SVG
    print "Export the chart to SVG file (%s.svg)" % _CHART_FILE
    chart.render_to_file(_CHART_FILE + ".svg")

    # Export the chart to PNG
    print "Export the chart to SVG file (%s.png)" % _CHART_FILE
    chart.render_to_png(_CHART_FILE + ".png")
