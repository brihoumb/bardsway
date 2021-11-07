# -*- coding: utf-8 -*-
'''
Python unittest for ffmpeg.
'''

import os
import unittest

from sub_module import ffmpeg_call


class TestFFmpeg(unittest.TestCase):

    def test_all_good(self):
        ffmpeg = ffmpeg_call.FFMPEG('/tmp')
        self.assertEqual(ffmpeg.install(), 0)

    def test_install_ffmpeg(self):
        save = os.environ['PATH']
        os.environ['PATH'] = ''
        ffmpeg = ffmpeg_call.FFMPEG('/tmp')
        self.assertEqual(ffmpeg.install(), 0)
        os.environ['PATH'] = save

    def test_archive_exist(self):
        save = os.environ['PATH']
        os.environ['PATH'] = ''
        open('/tmp/ffmpeg_amd64.zip', 'a').close()
        ffmpeg = ffmpeg_call.FFMPEG('/tmp')
        self.assertEqual(ffmpeg.install(), 1)
        os.environ['PATH'] = save
        os.remove('/tmp/ffmpeg_amd64.zip')


if __name__ == '__main__':
    unittest.main()
