import os
import sys
import time
import logging
import requests
import datetime
from zipfile import ZipFile

from hurry.filesize import size


MODEL_URL = 'https://github.com/brihoumb/bardsway/releases/' +\
            'download/beta2.0/mt.model.zip'
THRESHOLD_URL = 'https://github.com/brihoumb/bardsway/releases/' +\
                'download/beta2.0/threshold.p'


def countdown(chunk):
    global start, downloaded, total_size
    downloaded += len(chunk)
    duration = time.time() - start
    if round(duration, 1).is_integer():
        sys.stdout.write("\033[K")
        duration = datetime.timedelta(seconds=int(duration))
        print(f'[{duration}]: {size(downloaded)}' +
              f'/{total_size}', end='\r')


def download_threshold(path):
    logging.info(f'-$- Downloading threshold at {THRESHOLD_URL} -$-')
    try:
        response = requests.get(THRESHOLD_URL, stream=True,
                                headers={}, data={})
        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
            file.close()
        return 0
    except requests.exceptions.HTTPError as err:
        logging.critical(f'-$- Download error: {err.code}:' +
                         f'{err.reason} -$-')
        sys.exit(1)


def extract(archive, path):
    with ZipFile(archive) as zipObj:
        zipObj.extractall(path)
        zipObj.close()
        os.remove(archive)


def download_model(path):
    logging.info(f'-$- Downloading model at {MODEL_URL} -$-')
    model_archive = os.path.join(path, 'mt.model.zip')
    try:
        response = requests.get(MODEL_URL, stream=True, headers={}, data={})
        global start, downloaded, total_size
        start = time.time()
        downloaded = 0
        total_size = size(int(response.headers.get('content-length')))
        with open(model_archive, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                countdown(chunk)
                file.write(chunk)
            file.close()
        extract(model_archive, path)
        return 0
    except requests.exceptions.HTTPError as err:
        logging.critical(f'-$- Download error: {err.code}:' +
                         f'{err.reason} -$-')
        sys.exit(1)
