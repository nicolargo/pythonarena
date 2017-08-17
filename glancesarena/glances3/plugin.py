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

logging.basicConfig(level=logging.INFO,
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


class Plugin:
    def __init__(self, name):
        logging.info('Init plugin {}'.format(name))
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
    def update(self, item):
        """Simulate an plugin update method."""
        logging.info('Update processe started')
        # Simulate an update
        t = Timer(random.uniform(0, 5))
        while not t.finished() and not self.stopped():
            sleep(0.01)
            self._stats.append(item)
        # /Simulate an update
        if self.stopped():
            logging.info('Update processes stopped')
        else:
            logging.info('Update method done')
