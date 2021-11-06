#!/usr/bin/env python

import sys
import json
import time
import logging
import platform
import threading
from os.path import join, abspath, dirname, isfile

import sciter
from gui.src import home
from gui.src import results
from gui.src import options
from entrypoint import bardsway_entrypoint


class Frame(sciter.Window):
    loaded = False
    locked = False
    thread_bw = None
    mutex = threading.Lock()

    def __init__(self, path):
        super().__init__(ismain=True, uni_theme=True)
        self.set_dispatch_options(enable=True, require_attribute=False)
        pass

    def isLoaded(self, state=False):
        if state:
            self.loaded = state
        else:
            return self.loaded
        pass

    def isLocked(self):
        return self.locked

    def hasStarted(self, state=None):
        if not state:
            return home.has_started()
        return home.has_started(state.get_value())

    def platform(self):
        return platform.system()

    def listFiles(self, filename='.'):
        return results.list_files(join(self.loadConfig()[3],
                                  filename.get_value()))

    def listDirs(self):
        return results.list_dir(self.loadConfig()[3])

    def retrieveOscillogram(self, filename):
        return results.get_audio_oscillogram(join(self.loadConfig()[3],
                                                  filename.get_value()))

    def getAudioPath(self, filename):
        return join(self.loadConfig()[3], filename.get_value())

    def init_entrypoint(self, path):
        self.mutex.acquire()
        logging.info("--- Lock mutex ---")
        self.locked = True
        try:
            bardsway_entrypoint(path.get_value())
        finally:
            self.mutex.release()
            logging.info("--- Release mutex ---")
            self.locked = False

    def startBardsway(self, path):
        if not self.locked:
            self.kill()
            if self.thread_bw is None or not self.thread_bw.isAlive():
                self.thread_bw = threading.Thread(None, self.init_entrypoint,
                                                  None, (path,))
                self.thread_bw.start()
        pass

    def kill(self):
        if self.thread_bw is not None and not self.thread_bw.isAlive():
            try:
                self.thread_bw.join()
                self.thread_bw = None
            except RuntimeError:
                self.thread_bw = None
                pass
        pass

    def editPage(self):
        home.retrieve_log(self.get_root())
        pass

    def loadConfig(self):
        return options.load_config()

    def loadCredentials(self):
        return options.load_credentials()

    def getExpiration(self, key=None):
        if key is not None:
            return options.check_new_key(key.get_value())
        return options.get_expiration()

    def setupConfig(self, file):
        options.setup_config(file.get_value())
        pass

    def updateConfig(self, folder, target):
        options.update_config(folder.get_value(), target.get_value())
        pass

    def updateCredentials(self, email, password):
        options.update_credentials(email.get_value(), password.get_value())
        pass

    def pause(self, s):
        time.sleep(s.get_value())
        pass


def start_sciter(dir_name):
    sciter.runtime_features(file_io=True, allow_sysinfo=True)
    frame = Frame(dir_name)
    try:
        frame.load_file(join(dir_name, 'front', 'home.html'))
    except sciter.error.SciterError:
        frame.load_file(join(dir_name, 'gui', 'front', 'home.html'))
    frame.run_app()
    frame.kill()
