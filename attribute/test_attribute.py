#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Test of the attribute.py
#

import unittest
from time import sleep

from attribute import Attribute

class TestAttribute(unittest.TestCase):

    """Test Glances class."""

    def setUp(self):
        """The function is called *every time* before test_*."""
        # print('\n' + '=' * 78)
        pass

    def test_000_nominal(self):
        a = Attribute('stat')
        self.assertEqual(a.name, 'stat')

        a.name = 'stat2'
        self.assertEqual(a.name, 'stat2')

        self.assertIsNone(a.value)
        self.assertEqual(a.history, [])

        a.value = 1
        self.assertEqual(a.value, 1)
        self.assertEqual(a.history, [])
        a.value = 2
        self.assertEqual(a.value, 2)
        self.assertEqual(a.history, [1])
        a.value = 3
        self.assertEqual(a.value, 3)
        self.assertEqual(a.history, [1, 2])

        self.assertEqual(a.history_mean(3), 1.0)

    def test_001_withmaxsize(self):
        a = Attribute('stat3', history_max_size=5)
        self.assertEqual(a.name, 'stat3')

        for i in xrange(0, 8):
            a.value = i
        self.assertEqual(a.history, [2, 3, 4, 5, 6])

    def test_002_withrate(self):
        a = Attribute('stat4', is_rate=True)
        self.assertEqual(a.name, 'stat4')

        a.value = 1
        sleep(1)
        self.assertIsNone(a.value)
        a.value = 2
        sleep(1)
        self.assertAlmostEqual(a.value, 1, places=2)
        a.value = 3
        sleep(0.5)
        self.assertAlmostEqual(a.value, 1, places=2)
        a.value = 4
        sleep(2)
        self.assertAlmostEqual(a.value, 2, places=2)
        a.value = 5
        self.assertAlmostEqual(a.value, 0.5, places=2)

        self.assertAlmostEqual(a.history_mean(3), 6.0, places=1)


if __name__ == '__main__':
    unittest.main()
