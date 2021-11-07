# -*- coding: utf-8 -*-
'''
Python unittest for spleeter.
'''

import os
import shutil
import hashlib
import unittest

from sub_module import spleeter_call


class TestSpleeter(unittest.TestCase):

    def test_config_error(self):
        if os.path.exists('/tmp/6stems.json'):
            os.remove('/tmp/6stems.json')
        os.environ['MODEL_PATH'] = '/tmp/pretrained_models'
        spleeter = spleeter_call.Spleeter('/tmp', '6stems')
        self.assertEqual(spleeter.install(), 1)

    def test_model_error(self):
        if os.path.exists('/tmp/7stems.json'):
            os.remove('/tmp/7stems.json')
        os.environ['MODEL_PATH'] = '/tmp/pretrained_models'
        open('/tmp/7stems.json', 'a').close()
        spleeter = spleeter_call.Spleeter('/tmp', '7stems')
        self.assertEqual(spleeter.install(), 1)

    def test_all_good(self):
        if os.path.exists('/tmp/ffmpeg'):
            shutil.rmtree('/tmp/ffmpeg')
        os.environ['MODEL_PATH'] = '/tmp/pretrained_models'
        spleeter = spleeter_call.Spleeter('/tmp', '5stems')
        self.assertEqual(spleeter.install(), 0)
        spleeter.execute('/tmp/test.wav', '/tmp')
        with open('/tmp/test/piano.wav', 'rb') as file:
            bytes = file.read()
            file.close()
            hash = hashlib.md5(bytes).hexdigest()
            self.assertEqual(hash, '1c8fce3aa0367c5e935ab38b427e0fa8')


if __name__ == '__main__':
    unittest.main()
