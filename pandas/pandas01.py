#!/usr/bin/env python
#
# Test Panda lib
# Read CSV file
#

__appname__ = 'panda01'
__version__ = "0.1"
__author__ = "Nicolas Hennion <nicolas@nicolargo.com>"
__licence__ = "LGPL"

# Libs
#=====

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# input_file = 'input.tsv'
input_file = '/home/nicolargo/tmp/WE1.AOCS._NS_OCC.2013.012.tsv'

i = pd.read_csv(input_file, sep='\t', comment='#',  index_col=0, parse_dates=True, infer_datetime_format=True, error_bad_lines=False, squeeze=True)

# print(i)

# print(i.dtypes)

# with open("/tmp/pandas.html", "w") as f:
#     f.write(i.to_html())

# i.to_pickle("/tmp/pandas.pkl")
# i2 = pandas.read_pickle("/tmp/pandas.pkl")
# print(i == i2)

# print(i['TB00002K'])
# print(i['13-01-2014_00:11:31.620':'19-01-2014_23:59:30.647'])
# print(i['13-01-2014_00:11:31.620':'19-01-2014_23:59:30.647']['TB00002K'])
# print(i[i.TB00002K > 14.0])

print(i['AE01G'])
print(i.min())
print(i.max())
# print(i.mean())

i.plot()

# s = i.ix[0,:]
# print(s)

# print(s.resample('1D', how='mean'))