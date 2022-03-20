#!/usr/bin/env python
#
# Test the curses lib
#
# Needed for Glances UI
# - Add a line
# - Add a column
# - Add an item for a line
# - Add an item to a column
# - set/get item size
# - set/get line size

import curses
import traceback
import locale

locale.setlocale(locale.LC_ALL, '')
encoding = locale.getpreferredencoding()


class MyItem(object):

    def __init__(self, win, pos='STD', xpos=0, ypos=0, xsize=0, ysize=0):
        """
        Init an item size xsize*ysize
        Position:
        pos = STD > xpos, ypos (this is the default)
        pos = LEFT > left, ypos
        pos = XCENTER > middle, ypos
        pos = RIGHT > right, ypos
        pos = TOP > xpos, top
        pos = YCENTER > xpos, middle
        pos = BOTTOM > xpos, bottom
        """
        self.win = win
        self.pos = pos
        self.xpos = xpos
        self.ypos = ypos
        self.xsize = xsize
        self.ysize = ysize
        self.current_line = 0
        self.last_xsize = -1
        self.last_ysize = -1
        self.update()

    def update(self):
        # Put window cursor to the first line
        self.current_line = 0

        # Get window size
        win_xsize = self.win.getmaxyx()[1]
        win_ysize = self.win.getmaxyx()[0]

        if ((win_xsize != self.last_xsize)
                or (win_ysize != self.last_ysize)):
            # New windows size or init
            self.last_xsize = win_xsize
            self.last_ysize = win_ysize

            # Set item position
            if self.pos == "STD":
                pass
            elif self.pos == "LEFT":
                self.xpos = 0
            elif self.pos == "XCENTER":
                self.xpos = win_xsize / 2 - self.xsize / 2
            elif self.pos == "RIGHT":
                self.xpos = win_xsize - self.xsize
            elif self.pos == "TOP":
                self.ypos = 0
            elif self.pos == "YCENTER":
                self.ypos = win_ysize / 2 - self.ysize / 2
            elif self.pos == "BOTTOM":
                self.ypos = win_ysize - self.ysize
            elif self.pos == "LEFT_TOP":
                self.xpos = 0
                self.ypos = 0
            elif self.pos == "LEFT_YCENTER":
                self.xpos = 0
                self.ypos = win_ysize / 2 - self.ysize / 2
            elif self.pos == "LEFT_BOTTOM":
                self.xpos = 0
                self.ypos = win_ysize - self.ysize
            elif self.pos == "RIGHT_TOP":
                self.xpos = win_xsize - self.xsize
                self.ypos = 0
            elif self.pos == "RIGHT_YCENTER":
                self.xpos = win_xsize - self.xsize
                self.ypos = win_ysize / 2 - self.ysize / 2
            elif self.pos == "RIGHT_BOTTOM":
                self.xpos = win_xsize - self.xsize
                self.ypos = win_ysize - self.ysize

            # Do it...
            self.item = self.win.subpad(self.ysize, self.xsize, self.ypos, self.xpos)

    def write(self, text, style=curses.A_NORMAL):
        self.win.addnstr(self.ypos + self.current_line, self.xpos, text, len(text), style)
        self.current_line += 1

    def draw(self, ch):
        self.update()
        self.write("OK: {}".format(ch), curses.A_NORMAL | curses.color_pair(2))
        self.write("CAREFULL", curses.A_NORMAL | curses.color_pair(3))
        self.write("WARNING", curses.A_NORMAL | curses.color_pair(4))
        self.write("CRITICAL", curses.A_NORMAL | curses.color_pair(5))


class MyTerm(object):

    def __init__(self):
        """
        Init the curse terminal
        """
        # Init window
        try:
            self.screen = curses.initscr()
            curses.noecho()
            curses.cbreak()
            self.screen.keypad(1)
        except:
            self.end()
            traceback.print_exc()

        if hasattr(curses, 'start_color'):
            curses.start_color()
        if hasattr(curses, 'use_default_colors'):
            curses.use_default_colors()

        # OK
        curses.init_color(2, 0, 1000, 0)
        # CAREFULL
        curses.init_color(3, 0, 500, 1000)
        # WARNING
        curses.init_color(4, 1000, 500, 0)
        # CRITICAL
        curses.init_color(5, 1000, 0, 0)

        curses.init_pair(2, 2, -1)
        curses.init_pair(3, 3, -1)
        curses.init_pair(4, 4, -1)
        curses.init_pair(5, 5, -1)

        self.win = self.screen.subwin(0, 0)
        # Init items
        self.items = {}
        # First draw
        self.draw('INIT')

    def add_item(self, name, pos="LEFT", ypos=0, xsize=10, ysize=10):
        """
        Add item to  items dict
        """
        self.items[name] = MyItem(self.win, pos=pos, ypos=ypos, xsize=xsize, ysize=ysize)

    def end(self):
        """
        Get back to initial terminal
        """
        curses.nocbreak()
        self.screen.keypad(0)
        curses.echo()
        curses.endwin()

    def draw(self, ch):
        """
        Draw and refresh the screen
        """
        # Erase the screen
        self.screen.erase()
        # Draw all items
        for item in self.items:
            self.items[item].draw(ch)
        # then refresh the window
        self.win.refresh()

    def handle(self):
        """
        Main loop
        """
        self.win.timeout(1000)
        while True:
            ch = self.win.getch()
            if ch == ord('q') or ch == 27:
                break
            self.draw(ch)


def main():
    myterm = MyTerm()
    myterm.add_item('cpu', pos="LEFT", ypos=0, xsize=10, ysize=10)
    myterm.add_item('load', pos="XCENTER", ypos=0, xsize=10, ysize=10)
    myterm.add_item('mem', pos="RIGHT", ypos=0, xsize=10, ysize=10)
    myterm.add_item('net', pos="LEFT_YCENTER", xsize=20, ysize=10)
    myterm.add_item('fs', pos="LEFT_BOTTOM", xsize=20, ysize=10)
    myterm.add_item('proc', pos="RIGHT_BOTTOM", xsize=40, ysize=20)

    # Run the main loop
    myterm.handle()

    myterm.end()


if __name__ == "__main__":
    main()
