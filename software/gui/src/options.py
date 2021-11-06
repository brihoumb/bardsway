import os
import sys
import json
import requests
from os.path import join, abspath, dirname, isfile, basename

from gui.src.rsa_encrypt import BardswayRSA


rsa_encryptor = BardswayRSA()


def setup_config(file):
    data = {
        'path': {
            'rdn': join(os.environ.get('BW_PATH', '.'),
                        'models', 'note_recognition_model'),
            'ffmpeg': join(os.environ.get('BW_PATH', '.'), 'ffmpeg'),
            'result': join(os.environ.get('BW_PATH', '.'), 'analysis'),
            'spleeter': join(os.environ.get('BW_PATH', '.'),
                             'models', 'pretrained_models')
        },
        'credentials': {
            'email': '',
            'password': '',
            'expirationDate': ''
        }
    }
    json.dump(data, file, indent=2)


def load_config():
    bw_path = os.environ.get('BW_PATH')
    if bw_path and basename(bw_path) == 'libs':
        conf = join(bw_path, '..', 'config.json')
    else:
        conf = join(os.environ.get('BW_PATH', '.'), 'config.json')
    file = isfile(conf)
    if not file or os.path.getsize(conf) == 0:
        file = open(conf, '+w')
        setup_config(file)
        file.close()
        load_config()
    with open(conf, 'r') as file:
        f = file.read()
        f = json.loads(f)['path']
        ret = [f['ffmpeg'], f['rdn'], f['spleeter'], f['result']]
        file.close()
    return ret


def load_credentials():
    bw_path = os.environ.get('BW_PATH')
    if bw_path and basename(bw_path) == 'libs':
        conf = join(bw_path, '..', 'config.json')
    else:
        conf = join(os.environ.get('BW_PATH', '.'), 'config.json')
    file = isfile(conf)
    if not file or os.path.getsize(conf) == 0:
        file = open(conf, '+w')
        setup_config(file)
        file.close()
    with open(conf, 'r') as file:
        f = file.read()
        f = json.loads(f)['credentials']
        file.close()
    return f


def check_new_key(key):
    credentials = load_credentials()
    url = 'https://dry-eyrie-23104.herokuapp.com/login'
    payload = {'email': credentials['email'],
               'password': rsa_encryptor.decrypt(credentials['password'])}
    response = requests.request('POST',
                                url,
                                headers={'Content-Type': 'application/json'},
                                data=json.dumps(payload))
    if response.json()['responseType'] == 'Unauthorized' or\
       response.json()['user']['licenseKey'] != key:
        return 'Unauthorized'
    else:
        url = 'https://dry-eyrie-23104.herokuapp.com/activatekey'
        requests.request('GET',
                         url,
                         headers={'Content-Type': 'application/json'},
                         data=json.dumps(payload))
        update_credentials(payload["email"], payload["password"],
                           response.json()['user']['licenseExpirationDate'])
        return response.json()['user']['licenseExpirationDate']


def get_expiration():
    credentials = load_credentials()
    url = 'https://dry-eyrie-23104.herokuapp.com/login'
    payload = {'email': credentials['email'],
               'password': rsa_encryptor.decrypt(credentials['password'])}
    response = requests.request('POST',
                                url,
                                headers={'Content-Type': 'application/json'},
                                data=json.dumps(payload))
    if response.json()['responseType'] == 'Unauthorized':
        return "Unauthorized"
    else:
        update_credentials(payload["email"], payload["password"],
                           response.json()['user']['licenseExpirationDate'])
        return response.json()['user']['licenseExpirationDate']


def get_field(target):
    bw_path = os.environ.get('BW_PATH')
    if bw_path and basename(bw_path) == 'libs':
        conf = join(bw_path, '..', 'config.json')
    else:
        conf = join(os.environ.get('BW_PATH', '.'), 'config.json')
    file = isfile(conf)
    if not file or os.path.getsize(conf) == 0:
        file = open(conf, '+w')
        setup_config(file)
        file.close()
    with open(conf, 'r') as file:
        f = file.read()
        f = json.loads(f)['path']
        file.close()
    return f[target]


def update_config(folder, target):
    bw_path = os.environ.get('BW_PATH')
    if bw_path and basename(bw_path) == 'libs':
        conf = join(bw_path, '..', 'config.json')
    else:
        conf = join(os.environ.get('BW_PATH', '.'), 'config.json')
    with open(conf, 'r') as file:
        f = file.read()
        f = json.loads(f)
        f['path'][target] = folder
        file.close()
    with open(conf, 'w') as file:
        file.write(json.dumps(f, indent=2))
        file.close()


def update_credentials(email, password, expiration=''):
    bw_path = os.environ.get('BW_PATH')
    if bw_path and basename(bw_path) == 'libs':
        conf = join(bw_path, '..', 'config.json')
    else:
        conf = join(os.environ.get('BW_PATH', '.'), 'config.json')
    with open(conf, 'r') as file:
        f = file.read()
        f = json.loads(f)
        f['credentials']['email'] = email
        f['credentials']['password'] = rsa_encryptor.encrypt(password)
        f['credentials']['expirationDate'] = expiration
        file.close()
    with open(conf, 'w') as file:
        file.write(json.dumps(f, indent=2))
        file.close()
