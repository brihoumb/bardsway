import os
import json
import shutil
import zipfile
import hashlib
import requests
from threading import Thread
from platform import system as which
from os.path import realpath, join, abspath, dirname, isfile, basename, exists

import sciter
from checksumdir import dirhash

from software_installer.src.uninstall import add_to_path
from software_installer.src.rsa_encrypt import BardswayRSA


_path = ''
_urls = {}
_sums = {}
_dlWin = 4
_dlFail = 0
_bar = None
_logger = None
_HTMLroot = None
_bar_level = None
_isUpdate = False
_isWindows = False
_thread_list = list()
_rsa_encryptor = BardswayRSA()
_sourceURLS = 'https://raw.githubusercontent.com/brihoumb/' +\
              'bardsway/master/urls.json'
_sourceSums = 'https://raw.githubusercontent.com/brihoumb/' +\
              'bardsway/master/checksums.json'


def init():
    global _isWindows
    _path = realpath(__file__)
    _isWindows = True if which() == 'Windows' else False


def io(str):
    _logger.append(sciter.Element.create('p', f'{str}'))


def io_setup(root):
    global _HTMLroot, _bar, _bar_level, _logger
    _HTMLroot = root
    _bar = _HTMLroot.find_first('#progress-bar')
    _bar_level = int(_bar.style_attribute('width')[:-1])
    _logger = _HTMLroot.find_first('#logger')
    io('Initializing ...')


def progress_bar(advance):
    global _bar, _bar_level
    if (_bar_level + advance >= 100):
        advance = 100 - _bar_level
    _bar.set_style_attribute('width', f'{_bar_level + advance % 99}%')
    _bar_level = _bar_level + advance


# ============= Setup Installation ================


def set_install_path(path):
    global _path
    _path = path


def init_install(root):
    global _path
    if basename(_path) == 'bardsway':
        _path = _path
    else:
        _path = join(_path, 'bardsway')
    io_setup(root)
    build_arch()


def start(root):
    global _path, _HTMLroot
    io_setup(root)
    build_arch()
    load_links()
    if _isUpdate:
        update_bardsway()
    else:
        install_bardsway()


def build_arch():
    global _path, _isUpdate
    io('Building architecture.')
    if os.path.exists(_path):
        _isUpdate = True
        io('Check for update.')
        return
    else:
        os.mkdir(_path)
    if not os.path.exists(join(_path, 'models')):
        os.mkdir(join(_path, 'models'))
    symlink = join(_path, f'bardsway{".exe" if _isWindows else ""}')
    if not exists(symlink):
        os.symlink(add_to_path(symlink, 'libs'), symlink)
    setup_config()
    progress_bar(1)


def load_links():
    global _urls, _sums
    files = [join(_path, 'urls.json'), join(_path, 'checksums.json')]
    sources = [_sourceURLS, _sourceSums]
    io('Retrieve urls and checksums files.')
    for i in range(2):
        try:
            with requests.get(sources[i], allow_redirects=True) as res:
                if res.status_code != 200:
                    io('Error happened while downloading' +
                       f'{direname(sources[i])}: {res.status_code}')
                    return
                with open(files[i], 'w') as outfile:
                    if i:
                        _sums = res.json()
                        json.dump(_sums, outfile)
                    else:
                        _urls = res.json()
                        json.dump(_urls, outfile)
                    outfile.close()
        except requests.exceptions.HTTPError as err:
            io('Error happened while downloading' +
               f'{direname(sources[i])}: {err.code}: {err.reason}')


# ============= Detect Installation or setup ================


def install_bardsway():
    global _dlWin
    if shutil.which('ffmpeg') is None:
        file = f'ffmpeg_{("window" if _isWindows is True else "linux")}.zip'
        _thread_list.append(Thread(target=download,
                                   args=(_urls[file],
                                         _path,
                                         file)))
    else:
        _dlWin -= 1
        progress_bar(9)
    files = [
        f'bardsway_{("windows" if _isWindows is True else "linux")}.zip',
        'spleeter_model.zip',
        'note_recognition_model.zip'
    ]
    for file in files:
        if file == 'bardsway_linux.zip' or file == 'bardsway_windows.zip':
            location = _path
        else:
            location = join(_path, 'models')
        _thread_list.append(Thread(target=download,
                                   args=(_urls[file],
                                         location,
                                         file)))
    for thread in _thread_list:
        thread.start()
        io(f'Starting threads {thread.getName()}')


def download(url, storage, filename, zip=True):
    global _dlFail, _dlWin
    ret = True
    try:
        io(f'Downloading {filename}.')
        with requests.get(url, allow_redirects=True) as res:
            if res.status_code != 200:
                io('Error happened while downloading ' +
                   f'{filename}: {res.status_code}.')
                return
            if not exists(join(storage + dirname(filename))):
                os.mkdir(join(storage + dirname(filename)))
            with open(join(storage, filename), 'wb') as f:
                f.write(res.content)
        io(f'{filename} succesfully downloaded.')
        progress_bar(9)
        if zip:
            ret = extract_zip(storage, filename, zip)
        else:
            _dlWin = _dlWin - 1
            ret = checksum(storage, filename, zip)
            if ret:
                progress_bar(9)
    except requests.exceptions.HTTPError as err:
        io(f'Error happened while downloading ' +
           f'{filename}: {err.code} - {err.reason}.')
        _dlFail = _dlFail - 1
    if _dlWin + _dlFail == 0:
        ending()
    return


def checksum(storage, filename, zip=False):
    global _sums
    ret = True
    with open(join(storage, filename), 'rb') as file:
        bytes = file.read()
        file.close()
        sum = hashlib.md5(bytes).hexdigest()
        if filename == 'ffmpeg_windows.zip':
            filename = 'ffmpeg_window.zip'
        if (_sums[filename if zip else filename[7:]] != sum):
            io(f'/!\\ Invalid hash: {filename} must be updated. /!\\')
            ret = False
    io(f'checksum {filename} OK')
    return ret


def extract_zip(storage, filename, zip):
    global _dlFail, _dlWin
    try:
        if not checksum(storage, filename, zip):
            os.remove(join(storage, filename))
            return False
        with zipfile.ZipFile(join(storage, filename), 'r') as zip_ref:
            zip_ref.extractall(storage)
        os.remove(join(storage, filename))
        io(f'{filename} succesfully deflated')
        _dlWin = _dlWin - 1
        progress_bar(9)
        return True
    except zipfile.BadZipFile:
        io(f'Failed to deflate {filename}.')
        _dlFail = _dlFail - 1


# ============= Update ================


def update_bardsway():
    global _dlWin
    file = f'bardsway_{("windows" if _isWindows is True else "linux")}.zip'
    folder_checker(file, 'libs', True)
    if shutil.which('ffmpeg') is None:
        file = f'ffmpeg_folder_' +\
               f'{("windows" if _isWindows is True else "linux")}'
        folder_checker(file, 'ffmpeg', False, True)
    else:
        _dlWin -= 1
    file = 'spleeter_model.zip'
    if not folder_checker(file, join('models', 'pretrained_models')):
        file = 'spleeter_model.zip'
        file_checker(file, join('models', '5stems.json'))
    file = 'note_recognition_model.zip'
    if not folder_checker(file, join('models', 'note_recognition_model')):
        file = 'note_recognition_model.zip'
        file_checker(file, join('models', 'threshold.p'))
    for thread in _thread_list:
        thread.start()


def file_checker(file, localPath):
    global _dlWin
    if not exists(join(_path, localPath) or
       not checksum(_path, localPath, False)):
        dl = Thread(target=download,
                    args=(_urls[file], join(_path, file)))
        _thread_list.append(dl)
    else:
        io(f'{file} is up to date')


def folder_checker(file, localPath, bardscase=False, ffmcase=False):
    global _dlWin
    if bardscase and (not exists(join(_path, localPath)) or
       dirhash(join(_path, localPath)) != _sums[f'{localPath}_' +
       f'{("windows" if _isWindows is True else "linux")}'[1:]]):
        dl = Thread(target=download,
                    args=(_urls[file], _path, file))
        _thread_list.append(dl)
        return True
    elif ffmcase and (not exists(join(_path, localPath)) or
                      dirhash(join(_path, localPath)) != _sums[file]):
        file = file.replace('_folder', '').__add__('.zip')
        dl = Thread(target=download,
                    args=(_urls[file], _path, file))
        _thread_list.append(dl)
        return True
    elif bardscase or ffmcase:
        _dlWin = _dlWin - 1
        progress_bar(25)
        io(f'{file} is up to date')
        return False
    elif not exists(join(_path, localPath)) or\
            dirhash(join(_path, localPath)) != _sums[localPath[8:]]:
        dl = Thread(target=download,
                    args=(_urls[file], join(_path, 'models'), file))
        _thread_list.append(dl)
        return True
    else:
        _dlWin = _dlWin - 1
        progress_bar(25)
        io(f'{file} is up to date')
    return False


# ============= End ================


def ending():
    success = 'Bards Way is succesfully installed on your computer'
    failure = f'An error occured while installing Bard\'s Way: {-_dlFail}' +\
              'file(s) were not downloaded properly or encountered ' +\
              'an error during installation. Please try to reinstall ' +\
              'Bard\'s Way and feel free to contact us if the problem reoccurs'
    progress_bar(99)
    io(success if _dlWin == 0 else failure)
    os.remove(join(_path, 'urls.json'))
    os.remove(join(_path, 'checksums.json'))
    kill_thread()


def kill_thread():
    global _thread_list
    for thread in _thread_list:
        try:
            thread.join()
        except RuntimeError:
            pass
        io(f'{thread.getName()} down.')
    _thread_list.clear()


# ============= Credentials ================


def setup_config():
    io('Setting up configuration file.')
    data = {
        'path': {
            'rdn': join(_path, 'models', 'note_recognition_model'),
            'ffmpeg': join(_path, 'ffmpeg'),
            'result': join(_path, 'analysis'),
            'spleeter': join(_path, 'models', 'pretrained_models')
        },
        'credentials': {
            'email': '',
            'password': '',
            'expirationDate': ''
        }
    }
    conf = join(_path, 'config.json')
    if not isfile(conf):
        file = open(conf, '+w')
        json.dump(data, file, indent=2)
        file.close()


def load_credentials():
    global _path
    conf = join(_path, 'config.json')
    file = isfile(conf)
    if not file:
        setup_config()
    with open(conf, 'r') as file:
        f = file.read()
        f = json.loads(f)['credentials']
        file.close()
    return f


def get_expiration(key=None):
    credentials = load_credentials()
    url = 'https://dry-eyrie-23104.herokuapp.com/login'
    payload = {'email': credentials['email'],
               'password': _rsa_encryptor.decrypt(credentials['password'])}
    response = requests.request('POST',
                                url,
                                headers={'Content-Type': 'application/json'},
                                data=json.dumps(payload))
    if response.json()['responseType'] == 'Unauthorized' or\
       response.json()['user']['licenseKey'] != key:
        return 'Unauthorized'
    elif response.json()['user']['licenseExpirationDate'] == None:
        url = 'https://dry-eyrie-23104.herokuapp.com/activatekey'
        requests.request('GET',
                         url,
                         headers={'Content-Type': 'application/json'},
                         data=json.dumps(payload))
        return get_expiration()
    update_credentials(payload['email'], payload['password'],
                       response.json()['user']['licenseExpirationDate'])
    return response.json()['user']['licenseExpirationDate']


def update_credentials(email, password, expiration=''):
    conf = join(_path, 'config.json')
    with open(conf, 'r') as file:
        f = file.read()
        f = json.loads(f)
        f['credentials']['email'] = email
        f['credentials']['password'] = _rsa_encryptor.encrypt(password)
        f['credentials']['expirationDate'] = expiration
        file.close()
    with open(conf, 'w') as file:
        file.write(json.dumps(f, indent=2))
        file.close()
