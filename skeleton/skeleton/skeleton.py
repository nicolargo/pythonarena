#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Skeleton
# ...
#
# Copyright (C) 2013 Nicolargo <nicolas@nicolargo.com>
#
# Skeleton is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Skeleton is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

__appname__ = "Skeleton"
__version__ = "0.1"
__author__ = "Nicolas Hennion <nicolas@nicolargo.com>"
__licence__ = "LGPL"
# Syntax
__doc__ = '''\
Usage: skeleton [options]

...

Options:
    -h: Display help and exit
    -v: Display version and exit
    -V: Switch on debug mode (Verbose)
'''

# Import lib
import getopt
import sys
import logging

# Global variables
#...

# Limit import to class...
__all__ = [ ]


# Classes

class main(object):
    """
    ...
    """

    def __init__(self, language="eng"):
        pass


# Functions

def printSyntax():
    """
    Display the syntax of the command line
    """
    print(__doc__)


def printVersion():
    """
    Display the current software version
    """
    print(__appname__ + " version " + __version__)


def main():
    """
    Main function
    """

    global _DEBUG_
    _DEBUG_ = False

    # Manage args
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvV")
    except getopt.GetoptError as err:
        # Print help information and exit:
        print("Error: " + str(err))
        printSyntax()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h"):
            printVersion()
            printSyntax()
            sys.exit(0)
        elif opt in ("-v"):
            printVersion()
            sys.exit(0) 
        elif opt in ("-V"):
            _DEBUG_ = True
            # Verbose mode is ON
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s %(levelname)s - %(message)s',
                datefmt='%d/%m/%Y %H:%M:%S',
            )
        # Add others options here...
        else:
            printSyntax()
            sys.exit(0)

    # By default verbose mode is OFF
    if not _DEBUG_:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s - %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S',
        )
    logging.debug("Running %s version %s" % (__appname__, __version__))
    logging.debug("Debug mode is ON")

    # Test args
    #...

    # Main loop
    #...
    

# Main
#=====

if __name__ == "__main__":
    main()

# The end...
