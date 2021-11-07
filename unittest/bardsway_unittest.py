# -*- coding: utf-8 -*-
'''
Python unittest for BardsWay.
'''

import unittest

import bards_way


class TestBardsWay(unittest.TestCase):

    def test_wrong_file(self):
        self.assertEqual(bards_way.bards_way('bardsway', '/tmp/test.mp3'), 1)

    def test_ffmpeg_fail(self):
        self.assertEqual(bards_way.bards_way('bardsway', '/tmp/test.wav',
                                             '6stems', True), 1)

    def test_spleeter_fail(self):
        self.assertEqual(bards_way.bards_way('bardsway', '/tmp/test.wav',
                                             '6stems'), 1)

    def test_all_good(self):
        self.assertEqual(bards_way.bards_way('bardsway', '/tmp/test.wav'), 0)


if __name__ == '__main__':
    unittest.main()
