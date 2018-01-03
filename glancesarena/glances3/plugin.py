# -*- coding: utf-8 -*-
#
# POC for Glances 3 (Core)
#
# Nicolargo (08/2017)

from threading import Lock, Event
from functools import wraps

from time import time, sleep
import random

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s')


class Timer(object):

    """The timer class. A simple chronometer."""

    def __init__(self, duration):
        self.duration = duration
        self.start()

    def start(self):
        self.target = time() + self.duration

    def reset(self):
        self.start()

    def get(self):
        return self.duration - (self.target - time())

    def set(self, duration):
        self.duration = duration

    def finished(self):
        return time() > self.target


def lockandrun(function):
    """
    Decorator for method. Return a new method with the
    an acquired lock (self._lock), run it and releases
    the lock.
    """
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        with self._lock:
            return function(self, *args, **kwargs)
    return wrapper


def logpluginmethod(function):
    """
    Decorator to log plugin method.
    Use the self.stopped() method.
    """
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        logging.debug('Method %s started' % function.__name__)
        ret = function(self, *args, **kwargs)
        if self.stopped():
            logging.debug('Method %s stopped' % function.__name__)
        else:
            logging.debug('Method %s finished' % function.__name__)
        return ret
    return wrapper


class Plugin:
    def __init__(self, name):
        # logging.debug('>>> {}'.format(self.__class__.__name__))
        logging.debug('Init plugin {}'.format(name))
        # Event needed to stop properly the thread
        self._stopper = Event()
        # The lock for the current thread
        self._lock = Lock()
        # Pugin's name
        self._name = name
        # Plugin's stats
        self._stats = []

    def stop(self, timeout=None):
        """Stop the thread"""
        self._stopper.set()

    def stopped(self):
        """Return True is the thread is stopped"""
        return self._stopper.isSet()

    @lockandrun
    def get(self):
        # Is it needed to lock the class when the stats are getted ?
        return self._stats

    @logpluginmethod
    def display(self):
        stats = self.get()
        # Display stats...

    @lockandrun
    @logpluginmethod
    def update(self, item):
        """Simulate an plugin update method."""
        # t = Timer(random.uniform(0, 3))
        t = Timer(2)
        while not t.finished() and not self.stopped():
            sleep(0.01)
            self._stats.append(item)

    @logpluginmethod
    def export(self):
        stats = self.get()
        # Export stats...
