# -*- coding: utf-8 -*-
#
# POC for a quick folder size computation function
# Nicolargo (11/2015)
#

import os
# Use the built-in version of scandir/walk if possible, otherwise
# use the scandir module version
try:
    # For Python 3.5 or higher
    from os import scandir, walk
except ImportError:
    # For others...
    from scandir import scandir, walk

def folder_size(path='.'):
    """Return the size of the directory given by path

    path: <string>"""

    ret = 0
    for f in scandir(path):
        if f.is_dir() and (f.name != '.' or f.name != '..'):
            ret += folder_size(os.path.join(path, f.name))
        else:
            ret += f.stat().st_size

    return ret

if __name__ == '__main__':
    print folder_size('/home/nicolargo/dev')
