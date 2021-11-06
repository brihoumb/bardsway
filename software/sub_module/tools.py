# -*- coding: utf-8 -*-
'''
Various tools function.
'''

import os
import platform


def check_create_dir(dir):
    if os.path.exists(dir):
        pass
    else:
        os.makedirs(dir)
    return dir


def get_path(name):
    path = os.path.dirname(os.path.abspath(name))
    if platform.system() == 'Windows':
        sysex = '.exe'
    else:
        sysex = ''
    return (sysex, path)
