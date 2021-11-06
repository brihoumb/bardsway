#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Main of the Bard's way software.
'''

import os
import sys
import logging
from io import StringIO
from gui.src.main import start_sciter


if __name__ == '__main__':
    stream = StringIO()
    console = logging.StreamHandler(stream=stream)
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(asctime)s: %(message)s',
                                           '%H:%M:%S'))

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s:  %(levelname)s : %(message)s',
                        datefmt='%H:%M:%S')
    logging.getLogger('').addHandler(console)

    os.environ['BW_PATH'] = os.path.dirname(os.path.abspath(sys.argv[0]))
    start_sciter(os.environ['BW_PATH'])

    logging.getLogger('').removeHandler(console)
    console.close()
