# -*- coding: utf-8 -*-
#
# POC for Glances 3 (Core)
#
# Nicolargo (08/2017)
#
# Three main threads will be run by the core:
# - Update the stats (thanks to the Stats class). Each plugin will be running
#   in another thread.
# - (optionnaly) Display the stats (thanks to the Outputs class)
# - (optionnaly) Export the stats (thanks to the Exports class)

import signal
import threading
from plugin import Plugin


class TestPlugin(Plugin):
    pass


class Stats(object):

    def __init__(self):
        # Dict of plugins
        # key: Plugin name
        # value: Plugin instance
        self.plugins = {}

        # Init the plugins
        for i in range(1, 10):
            pname = 'plugin%s' % (i - 1)
            self.plugins[pname] = TestPlugin(name=pname)

    def update(self, timeout=3):
        # Init the threads list
        plugin_threads = []
        for pname, p in self.plugins.iteritems():
            t = threading.Thread(name=pname,
                                 target=p.update,
                                 args=('ITEM',))
            plugin_threads.append(t)

        # Start all the threads
        for p in plugin_threads:
            p.start()

        # Wait the end of thr threads
        for p in plugin_threads:
            p.join(timeout=timeout)
            if p.isAlive():
                # Process is still running
                # Kill it
                self.kill(p.name)
                p.join()

    def kill(self, thread_name):
        print("Kill thread", thread_name)
        self.plugins[thread_name].stop()

    def stop(self, signal, frame):
        for p in self.plugins:
            p.stop()


def main():
    s = Stats()
    signal.signal(signal.SIGINT, s.stop)
    s.update()


if __name__ == '__main__':
    main()
