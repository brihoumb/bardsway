# -*- coding: utf-8 -*-
'''
Spleeter integration in Bard's way.
'''

import os
import sys
import time
import tarfile
import logging
import requests
import datetime
from tempfile import NamedTemporaryFile

from tqdm import tqdm
from hurry.filesize import size
from spleeter.separator import Separator
from spleeter.utils.logging import enable_logging
from spleeter.model.provider.github import compute_file_checksum


enable_logging()
URL_CONFIG = 'https://raw.githubusercontent.com/deezer/spleeter/' +\
             '47b990e5f2dde57a8dcdfdc911e584f8c96442b3/spleeter/' +\
             'resources/'


class Spleeter:
    def __init__(self, path='.', stems='5stems'):
        self.__stems = stems
        self.__config_file = os.path.join(path, f'{self.__stems}.json')
        self.__model_folder = os.environ.get('MODEL_PATH',
                                             os.path.join(path,
                                                          'pretrained_models'))
        self.__sum = '25a1e87eb5f75cc72a4d2d5467a0a50a' +\
                     'c75f05611f877c278793742513cc7218'

    def __get_model(self):
        base = "https://github.com/deezer/spleeter/releases/download/v1.4.0/"
        url = f'{base}{self.__stems}.tar.gz'
        logging.debug('-+- Downloading spleeter model at: ' +
                      f'{base}{self.__stems}" -+-')
        with requests.get(url, stream=True, allow_redirects=True) as response:
            code = response.status_code
            if response.status_code != 200:
                logging.error(f'-+- Download error: {code} -+-')
                return 1
            archive = NamedTemporaryFile(delete=False)
            try:
                p_bar = tqdm(total=int(response.headers.get('content-length')),
                             unit_scale=True, ncols=60)
                with archive as stream:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            p_bar.update(stream.write(chunk))
                logging.info('-+- Validating archive checksum -+-')
                if compute_file_checksum(archive.name) != self.__sum:
                    logging.error('-+- File corrupted, please retry -+-')
                    return 1
                with tarfile.open(name=archive.name) as tar:
                    tar.extractall(path=os.path.join(self.__model_folder,
                                                     self.__stems))
                return 0
            except Exception:
                return 1
            finally:
                os.unlink(archive.name)

    def __countdown(self, chunk):
        self.__downloaded += len(chunk)
        duration = time.time() - self.__start
        if round(duration, 1).is_integer():
            sys.stdout.write("\033[K")
            duration = datetime.timedelta(seconds=int(duration))
            print(f'[{duration}]: {size(self.__downloaded)}/{self.__size}',
                  end='\r')

    def __get_config(self):
        try:
            logging.debug(f'-+- Downloading at: {URL_CONFIG}' +
                          f'{self.__stems} -+-')
            response = requests.get(f'{URL_CONFIG}{self.__stems}.json',
                                    stream=True, headers={}, data={})
            if response.status_code != 200:
                code = response.status_code
                logging.error(f'-+- Download error: {code} -+-')
                return 1
            self.__start = time.time()
            self.__downloaded = 0
            self.__size = size(int(response.headers.get('content-length')))
            with open(self.__config_file, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    self.__countdown(chunk)
                    file.write(chunk)
                file.close()
            return 0
        except requests.exceptions.HTTPError as err:
            logging.error(f'-+- Download error: {err.code}:' +
                          f'{err.reason} -+-')
            return 1

    def install(self):
        if not os.path.exists(self.__model_folder) or\
           not os.path.exists(self.__config_file) or\
           len(os.listdir(self.__model_folder)) == 0 or\
           not os.path.exists(os.path.join(self.__model_folder, self.__stems)):
            logging.error(f'Error in spleeter: {self.__config_file} or' +
                          f'{self.__model_folder} not found')
            return 1
        if not os.path.exists(self.__config_file):
            if self.__get_config():
                logging.error('-+- Error in config file' +
                              f'{self.__config_file} -+-')
                return 1
        if not os.path.exists(self.__model_folder) or\
           len(os.listdir(self.__model_folder)) == 0 or\
           not os.path.exists(os.path.join(self.__model_folder, self.__stems)):
            if self.__get_model():
                logging.error('-+- Error in model' +
                              f'{self.__model_folder} not found -+-')
                return 1
        return 0

    def execute(self, filename, analysis_folder):
        separator = Separator(self.__config_file, multiprocess=False)
        separator.separate_to_file(filename, analysis_folder, synchronous=True)
