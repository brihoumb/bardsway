import sys
from os.path import join, abspath, dirname, isfile

import sciter

from software_installer.src import installer
from software_installer.src import uninstall


class Frame(sciter.Window):
    def __init__(self):
        super().__init__(ismain=True, uni_theme=True)
        self.set_dispatch_options(enable=True, require_attribute=False)
        installer.init()
        pass

    def getExpiration(self, key=None):
        if key is not None:
            return installer.get_expiration(key.get_value())
        return installer.get_expiration()

    def updateCredentials(self, email, password):
        installer.update_credentials(email.get_value(), password.get_value())
        pass

    def selectInstallPath(self, path):
        installer.set_install_path(path.get_value())
        pass

    def loadCredentials(self):
        return installer.load_credentials()

    def initInstall(self):
        installer.init_install(self.get_root())
        pass

    def install(self):
        installer.start(self.get_root())
        pass

    def uninstall(self, folder):
        return uninstall.uninstall(folder.get_value())


def start_sciter(dir_name):
    sciter.runtime_features(file_io=True, allow_sysinfo=True)
    root = abspath(dir_name)
    frame = Frame()
    try:
        frame.load_file(join(root, 'front', 'installer.html'))
    except Exception:
        frame.load_file(join(root, 'software_installer',
                             'front', 'installer.html'))
    frame.run_app()
