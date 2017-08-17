# -*- coding: utf-8 -*-
#
# POC for Glances 3 (Core)
#
# Nicolargo (08/2017)

import signal
import threading
from plugin import Plugin


class TestPlugin(Plugin):
    pass


class Stats(object):

    def __init__(self):
        # List of Plugin classes
        self.plugins_list = []

        # List of threads
        self.plugin_threads = []

        # Init plugins
        for i in range(1, 10):
            self.plugins_list.append(Plugin(name='plugin%s' % (i - 1)))

    def update(self):
        # Init the threads list
        self.plugin_threads = []
        for i in range(0, 9):
            t = threading.Thread(name='plugin%s' % i,
                                 target=self.plugins_list[i].update,
                                 args=(i,))
            self.plugin_threads.append(t)
            # Start all the threads
            t.start()
        # Wait all the threads
        t.join()

    def stop(self, signal, frame):
        for i in range(0, 9):
            self.plugins_list[i].stop()


def main():
    s = Stats()
    signal.signal(signal.SIGINT, s.stop)
    s.update()


if __name__ == '__main__':
    main()
