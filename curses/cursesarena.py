#!/usr/bin/env python
#
# Test the curses lib
#

import curses
import traceback
import time

class MyItem(object):
    
    def __init__(self, win, pos = 'STD', xpos = 0, ypos = 0, xsize = 0, ysize = 0):
        '''
        Init an item size xsize*ysize
        Position:
        pos = STD > xpos, ypos (this is the default)
        pos = LEFT > left, ypos
        pos = XCENTER > middle, ypos
        pos = RIGHT > right, ypos
        pos = TOP > xpos, top
        pos = YCENTER > xpos, middle
        pos = BOTTOM > xpos, bottom
        '''
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

        if ((win_xsize != self.last_xsize) \
            or (win_ysize != self.last_ysize)):
            # New windows size or init
            self.last_xsize = win_xsize
            self.last_ysize = win_ysize
    
            # Set item position
            if (self.pos == "STD"):
                pass
            elif (self.pos == "LEFT"):
                self.xpos = 0
            elif (self.pos == "XCENTER"):
                self.xpos = win_xsize / 2 - self.xsize / 2
            elif (self.pos == "RIGHT"):
                self.xpos = win_xsize - self.xsize
            elif (self.pos == "TOP"):
                self.ypos = 0
            elif (self.pos == "YCENTER"):
                self.ypos = win_ysize / 2 - self.ysize / 2
            elif (self.pos == "BOTTOM"):
                self.ypos = win_ysize - self.ysize
            elif (self.pos == "LEFT_TOP"):
                self.xpos = 0
                self.ypos = 0
            elif (self.pos == "LEFT_YCENTER"):
                self.xpos = 0
                self.ypos = win_ysize / 2 - self.ysize / 2
            elif (self.pos == "LEFT_BOTTOM"):
                self.xpos = 0
                self.ypos = win_ysize - self.ysize
            elif (self.pos == "RIGHT_TOP"):
                self.xpos = win_xsize - self.xsize
                self.ypos = 0
            elif (self.pos == "RIGHT_YCENTER"):
                self.xpos = win_xsize - self.xsize
                self.ypos = win_ysize / 2 - self.ysize / 2
            elif (self.pos == "RIGHT_BOTTOM"):
                self.xpos = win_xsize - self.xsize
                self.ypos = win_ysize - self.ysize
            
            # Do it...
            self.item = self.win.subpad(self.ysize, self.xsize, self.ypos, self.xpos)
    
    def write(self, text):
        self.win.addnstr(self.ypos+self.current_line, self.xpos, text, len(text))
        self.current_line += 1

    def draw(self):
        self.update()
#        self.item.border()
        self.write("Test")
        self.write("Test2")
        self.write("Test3")


class MyTerm(object):
    
    def __init__(self):
        '''
        Init the curse terminal
        '''
        # Init window
        try:
            self.screen = curses.initscr()
            curses.noecho()
            curses.cbreak()
            self.screen.keypad(1)
        except:
            self.end()
            traceback.print_exc()
        self.win = self.screen.subwin(0, 0)
        # Init items
        self.inititems()
        # First draw
        self.draw()
        # Run the main loop
        self.handle()
        
    def inititems(self):
        '''
        Init items
        '''
        self.items = {}
        self.items['cpu'] = MyItem(self.win, pos = "LEFT", ypos = 0, xsize = 10, ysize = 10)
        self.items['load'] = MyItem(self.win, pos = "XCENTER", ypos = 0, xsize = 10, ysize = 10)
        self.items['mem'] = MyItem(self.win, pos = "RIGHT", ypos = 0, xsize = 10, ysize = 10)
        self.items['net'] = MyItem(self.win, pos = "LEFT_YCENTER", xsize = 20, ysize = 10)
        self.items['fs'] = MyItem(self.win, pos = "LEFT_BOTTOM", xsize = 20, ysize = 10)
        self.items['proc'] = MyItem(self.win, pos = "RIGHT_BOTTOM", xsize = 40, ysize = 20)
        
    def end(self):
        '''
        Get back to initial terminal
        '''
        curses.nocbreak(); 
        self.screen.keypad(0); 
        curses.echo()
        curses.endwin()

    def draw(self):
        '''
        Draw and refresh the screen
        '''
        # Erase the screen
        self.screen.erase()
        # Draw all items
        for item in self.items:
            self.items[item].draw()
        # then refresh the window
        self.win.refresh()

    def handle(self):
        '''
        Main loop
        '''
        while True:
            ch = self.win.getch()
            if ch == ord('q'):
                break
            self.draw()
            
def main():
    myterm = MyTerm()
    myterm.end()

if __name__ == "__main__":
    main()