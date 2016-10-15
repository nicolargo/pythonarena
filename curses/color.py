#!/usr/bin/env python

class ANSIColors:
    RESET        = '\033[0m'
    WHITE        = '\033[1m'
    RED          = '\033[0;31m'
    GREEN        = '\033[0;32m'
    YELLOW       = '\033[0;33m'
    BLUE         = '\033[0;34m'
    MAGENTA      = '\033[0;35m'
    CYAN         = '\033[0;36m'
    GRAY         = '\033[0;30m'
    BOLD_RED     = '\033[1;31m'
    BOLD_GREEN   = '\033[1;32m'
    BOLD_YELLOW  = '\033[1;33m'
    BOLD_BLUE    = '\033[1;34m'
    BOLD_MAGENTA = '\033[1;35m'
    BOLD_CYAN    = '\033[1;36m'
    BOLD_GRAY    = '\033[1;30m'

def msg_color(msg, color):
    return (color + msg + ANSIColors.RESET)

print(msg_color("White", ANSIColors.WHITE))
print(msg_color("Red", ANSIColors.RED))
print(msg_color("Green", ANSIColors.GREEN))
print(msg_color("Yellow", ANSIColors.YELLOW))
print(msg_color("Blue", ANSIColors.BLUE))
print(msg_color("Magenta", ANSIColors.MAGENTA))
print(msg_color("Cyan", ANSIColors.CYAN))
print(msg_color("Gray", ANSIColors.GRAY))
print(msg_color("Bold red", ANSIColors.BOLD_RED))
print(msg_color("Bold green", ANSIColors.BOLD_GREEN))
print(msg_color("Bold yellow", ANSIColors.BOLD_YELLOW))
print(msg_color("Bold blue", ANSIColors.BOLD_BLUE))
print(msg_color("Bold magenta", ANSIColors.BOLD_MAGENTA))
print(msg_color("Bold cyan", ANSIColors.BOLD_CYAN))
print(msg_color("Bold gray", ANSIColors.BOLD_GRAY))
