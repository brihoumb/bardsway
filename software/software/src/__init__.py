import os
import sys
import logging
import platform
from software.src.download_lib import download

system = ';' if platform.system() == 'Windows' else ':'

if platform.system() == 'Windows':
    lib = 'sciter.dll'
else:
    lib = 'libsciter-gtk.so'

root = os.environ.get('BW_PATH', os.path.dirname(os.path.abspath(sys.argv[0])))
os.environ['PATH'] = f'{os.environ["PATH"]}{system}{root}'

if not os.path.exists(os.path.join(root, os.path.basename(lib))):
    if download(lib, os.path.join(root, lib)):
        logging.error("Could not retrieve library for OS")
        sys.exit(1)
