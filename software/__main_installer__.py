import os
import sys
from software_installer.src.main import start_sciter

if __name__ == '__main__':
    start_sciter(os.path.dirname(sys.argv[0]))
