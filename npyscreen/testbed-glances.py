# -*- coding: utf-8 -*-
#
# NPyScreen poc to replace Curses
# Nicolargo (03/2016)
#

import npyscreen

class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.registerForm("MAIN", TestForm(name="Glances", minimum_lines=24, minimum_columns=80))

class TestForm(npyscreen.Form):

    def create(self):
        self.add(npyscreen.TitleText, name="CPU:")
        self.keypress_timeout = 10

    def adjust_widgets(self):
        # KEYPRESSED
        pass

    def while_waiting(self):
        self.display()

if __name__ == "__main__":
    App = MyTestApp()
    App.run()
