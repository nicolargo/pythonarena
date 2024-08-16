#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Skeleton
# ...
#

__appname__ = "skeleton"
__version__ = "0.1"
__author__ = "Nicolas Hennion <nicolas@nicolargo.com>"
__licence__ = "MIT"

# Syntax exemples
__exemples__ = """\
Exemples:
"""

# Import lib
import argparse
import logging

# Configure default logger
logging.basicConfig(format="%(asctime)s %(levelname)8s - %(message)s")
logger = logging.getLogger(__appname__)
logger.setLevel(logging.INFO)

# Functions
# ==========


def main():
    """
    Main function
    """

    # Manage args
    parser = argparse.ArgumentParser(
        prog=__appname__,
        conflict_handler="resolve",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=__exemples__,
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=__appname__.capitalize() + " " + __version__,
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=False,
        dest="debug",
        help="enable debug mode",
    )

    args = parser.parse_args()

    # By default verbose mode is OFF
    if args.debug:
        logger.setLevel(logging.DEBUG)
    logger.debug("Running %s version %s" % (__appname__, __version__))
    logger.debug("Debug mode is ON")

    # Test args
    # ...

    # Main loop
    # ...


# Main
# =====

if __name__ == "__main__":
    main()

# The end...
