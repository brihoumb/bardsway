import os
import sys
import logging
import platform
from software_installer.src.download_lib import download

system = ';' if platform.system() == 'Windows' else ':'

if platform.system() == 'Windows':
    lib = 'sciter.dll'
else:
    lib = 'libsciter-gtk.so'

root = os.path.abspath(os.path.dirname(sys.argv[0]))
os.environ['PATH'] = f'{os.environ["PATH"]}{system}{root}'

if not os.path.exists(os.path.join(root, os.path.basename(lib))):
    if download(lib):
        logging.error("Could not retrieve library for OS")
        sys.exit(1)
