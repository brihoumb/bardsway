# -*- coding: utf-8 -*-
'''
FFMPEG class to init, download and install ffmpeg.
'''

import os
import sys
import time
import shutil
import hashlib
import logging
import datetime
import requests
from zipfile import ZipFile
from hurry.filesize import size
from platform import system as which


ZIP_WINDOWS = 'ffmpeg.zip'
ZIP_LINUX = 'ffmpeg_amd64.zip'
BASE_URL = 'https://github.com/brihoumb/bardsway/releases/download/beta2.0/'
SUM_LINUX = 'd296f89d97329e9b69253895cecc0006ff03e1fe0b6b24fbaede0e6232e8e508'
SUM_WINDOW = '4fe45672fbbade19f1a3ae5bcd81a1c2e81adbd46233a7310a4b7eefc8157d1c'


class FFMPEG:
    def __init__(self, path='.'):
        self.__folder = path
        self.__windows = True if which() == 'Windows' else False
        zip_name = ZIP_WINDOWS if self.__windows else ZIP_LINUX
        self.__url = f'{BASE_URL}{zip_name}'
        self.__archive = os.path.join(path, zip_name)
        self.__sum = SUM_WINDOW if self.__windows else SUM_LINUX

    def __change_env(self):
        logging.debug('-=- Check if ffmpeg in env or exists -=-')
        if (os.environ['PATH'].find('ffmpeg') == -1 or
           (os.path.exists(self.__folder) and
           len(os.listdir(self.__folder)) > 0)) and\
           shutil.which('ffmpeg') is None:
            logging.debug('-=- Set ffmepg to env -=-')
            os.environ['PATH'] += f'{";" if self.__windows else ":"}' +\
                                  os.path.join(self.__folder, 'bin') +\
                                  f'{";" if self.__windows else ":"}'
        logging.debug(f'-=- Found ffmpeg at {shutil.which("ffmpeg")} -=-')

    def __check_sum(self):
        with open(self.__archive, 'rb') as file:
            bytes = file.read()
            file.close()
            hash = hashlib.sha256(bytes).hexdigest()
            logging.debug('-=- Test if sha256sum differ -=-')
            if self.__sum != hash:
                logging.debug(f'{self.__sum} != {hash}')
                logging.error('OSError: Downloaded file is' +
                              ' corrupted, please retry')
                return 1
        return 0

    def __extract(self):
        logging.debug(f'-=- Extracting {self.__archive} -=-')
        with ZipFile(self.__archive) as zipObj:
            zipObj.extractall(self.__folder)
            zipObj.close()
            shutil.move(self.__folder, f'{self.__folder}o')
            shutil.move(os.path.join(f'{self.__folder}o', 'ffmpeg'),
                        f'{self.__folder}')
            os.rmdir(f'{self.__folder}o')
            os.remove(f'{self.__archive}')

    def __countdown(self, chunk):
        self.__downloaded += len(chunk)
        duration = time.time() - self.__start
        if round(duration, 1).is_integer():
            sys.stdout.write("\033[K")
            duration = datetime.timedelta(seconds=int(duration))
            print(f'[{duration}]: {size(self.__downloaded)}' +
                  f'/{self.__size}', end='\r')

    def __download(self):
        try:
            if os.path.exists(self.__archive):
                return 0
            logging.debug(f'-=- Downloading at: {self.__url} ' +
                          f'with hash: {self.__sum} -=-')
            response = requests.get(self.__url, stream=True,
                                    headers={}, data={})
            self.__start = time.time()
            self.__downloaded = 0
            self.__size = size(int(response.headers.get('content-length')))
            with open(self.__archive, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    self.__countdown(chunk)
                    file.write(chunk)
                file.close()
            return 0
        except requests.exceptions.HTTPError as err:
            logging.error(f'-=- Download error: {err.code}:' +
                          f'{err.reason} -=-')
            return 1

    def install(self):
        logging.info('-=- Check install of ffmpeg -=-')
        if shutil.which('ffmpeg') is None and \
           (not os.path.exists(self.__folder) or
           len(os.listdir(self.__folder)) <= 0):
            logging.error('-+- Error in ffmpeg' +
                          f'{self.__folder} not found not in path -+-')
            return 1
            if self.__download():
                logging.error('-+- Error in ffmpeg' +
                              f'{self.__folder} not found not in path -+-')
                return 1
            elif self.__check_sum():
                return 1
            self.__extract()
        self.__change_env()
        return 0
