# -*- coding: utf-8 -*-
'''
Python unittest for tools.
'''

import os
import sys
import unittest

from sub_module import tools


class TestTools(unittest.TestCase):

    def test_get_path(self):
        self.assertEqual(tools.get_path(sys.argv[0]),
                         ('', os.path.dirname(os.path.abspath(sys.argv[0]))))

    def test_check_create_dir(self):
        self.assertEqual(tools.check_create_dir('/tmp/toto'), '/tmp/toto')
        self.assertEqual(tools.check_create_dir('/tmp/toto'), '/tmp/toto')


if __name__ == '__main__':
    unittest.main()
