import sys
import threading
from os import listdir, mkdir, environ
from os.path import isfile, isdir, join, basename, dirname, exists

import pydub
from filetype import guess
import matplotlib.pyplot as plt


def list_files(result_path='.'):
    authorised_name = ['piano.wav',
                       'drums.wav',
                       'bass.wav',
                       'vocals.wav',
                       'other.wav']
    onlyfiles = [f for f in listdir(result_path)
                 if isfile(join(result_path, f)) and
                 guess(join(result_path, f)) is not None and
                 guess(join(result_path, f)).extension == 'wav' and
                 authorised_name.count(f)]
    return onlyfiles


def list_dir(result_path='.'):
    onlydir = [d for d in listdir(result_path) if isdir(join(result_path, d))]
    return onlydir


def get_audio_oscillogram(filename):
    oscillo = f'{environ.get("BW_PATH", ".")}/oscillo'
    music_name = basename(f'{dirname(filename)}_{basename(filename)[:-4]}')
    if not exists(oscillo):
        mkdir(oscillo)
    image_path = f'{join(oscillo, music_name)}.png'
    if not exists(image_path):
        a = pydub.AudioSegment.from_wav(filename).get_array_of_samples()
        lines = plt.plot(a)
        plt.axis('off')
        plt.setp(lines, color='#2B2B2B', linewidth=1)
        plt.savefig(f'{image_path}', format='png',
                    transparent=True, bbox_inches='tight')
        plt.close()
    return join('..', '..', image_path)
