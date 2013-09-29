#!/usr/bin/env python

from metaplugin import BasePlugin

class SecondPlugin(BasePlugin):
    """ My test plugin """

    def test(self):
        return "test"