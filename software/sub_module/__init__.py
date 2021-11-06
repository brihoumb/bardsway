import os
import sys
import platform
from gui.src.options import get_field

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
path = os.path.dirname(os.path.abspath(sys.argv[0]))
if platform.system() == 'Windows':
    sysex = 1
else:
    sysex = 0
os.environ['MODEL_PATH'] = get_field("spleeter")
