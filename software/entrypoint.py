#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Main file function and entrypoint.
'''

import os
import sys
import logging
from argparse import ArgumentParser

from bards_way import bards_way


def entrypoint():
    parser = ArgumentParser(description=('Bardsway is an instrumental' +
                                         'separation and recognition toolkit'))
    parser.add_argument('filename', nargs='?', type=str,
                        help=('Input audio file'))
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Debug mode')
    args = parser.parse_args()
    if not args.filename:
        return 1
    logging.info(f'-|- Starting Bard\'s Way with following args {args} -|-')
    return bards_way(sys.argv[0], args.filename)


def bardsway_entrypoint(filename):
    return bards_way(os.environ['BW_PATH'], filename)


if __name__ == '__main__':
    entrypoint()
