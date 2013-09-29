#!/usr/bin/env python

from metaplugin import BasePlugin

class FirstPlugin(BasePlugin):
    """ My test plugin """

    def test(self):
        return "test"
