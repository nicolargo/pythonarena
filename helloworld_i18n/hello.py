#!/usr/bin/env python

__appname__ = 'hello'
__version__ = "1.0"
__author__ = "Nicolas Hennion <nicolas@nicolargo.com>"
__licence__ = "LGPL"

import gettext
gettext.install(__appname__)

def main():
    print(_("Hello world !"))

if __name__ == "__main__":
    main()
