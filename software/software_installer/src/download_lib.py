import os
import hashlib
import logging
import requests
import platform


def compute_md5(lib):
    if platform.system() == 'Windows':
        sum = 'c8b57742f2e7b24c66baab5ad764f71f'
    else:
        sum = 'd152f5f9b04f4d05152bcc9e734ac9cf'
    with open(lib, 'rb') as file:
        bytes = file.read()
        file.close()
    return hashlib.md5(bytes).hexdigest() != sum


def download(lib_url):
    URI = 'https://github.com/brihoumb/bardsway/' +\
          f'releases/download/1.0.0/{lib_url}'
    with requests.get(URI, stream=True, allow_redirects=True) as response:
        if response.status_code != 200:
            logging.critical(f'-+- Download error: {response.status_code} -+-')
            return 1
        try:
            bin = open(os.path.basename(lib_url), 'wb')
            with bin as stream:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        stream.write(chunk)
            if compute_md5(os.path.basename(lib_url)):
                logging.critical('-+- File corrupted, please retry -+-')
                return 1
            return 0
        except Exception:
            return 1
