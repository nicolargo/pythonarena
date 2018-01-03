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

    def loop(self):
        update_thread = threading.Thread(name="update",
                                         target=self.update)
        export_thread = threading.Thread(name="export",
                                         target=self.export)
        display_thread = threading.Thread(name="display",
                                          target=self.display)

        update_thread.start()
        export_thread.start()
        display_thread.start()

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

        # Wait the end of the threads
        for p in plugin_threads:
            p.join(timeout=timeout)
            if p.isAlive():
                # Process is still running
                # Kill it
                self.kill(p.name)
                p.join()

    def export(self, timeout=3):
        for pname, p in self.plugins.iteritems():
            p.export()

    def display(self, refresh=3):
        for pname, p in self.plugins.iteritems():
            p.display()

    def kill(self, thread_name):
        self.plugins[thread_name].stop()

    def stop(self, signal, frame):
        for p in self.plugins:
            p.stop()


def main():
    s = Stats()
    signal.signal(signal.SIGINT, s.stop)
    s.loop()


if __name__ == '__main__':
    main()
