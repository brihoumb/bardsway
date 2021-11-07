# -*- coding: utf-8 -*-
'''
Bard's way core function.
'''

import os
import logging
import subprocess

from filetype import guess

from sub_module.ffmpeg_call import FFMPEG
from software.src.options import get_field
from sub_module.spleeter_call import Spleeter
from music_transcription.entrypoint import entrypoint
from sub_module.tools import check_create_dir, get_path


def bards_way(bin_name, filename, stems='5stems', ffmpeg=False):
    os.environ['MODEL_PATH'] = get_field("spleeter")
    logging.debug(f'--- File is {filename} ---')
    if guess(filename) is None or guess(filename).extension != 'wav':
        logging.critical('IOError: input file is not in WAV format!')
        return 1
    (extension, path) = get_path(bin_name)
    analysis_folder = check_create_dir(get_field("result"))
    logging.info('--- FFMPEG section ---')
    ffmpeg_mod = FFMPEG(get_field("ffmpeg"))
    if ffmpeg_mod.install() or ffmpeg:
        logging.critical('FFMPEGError: can\'t provide ffmpeg')
        return 1
    logging.info('--- FFMPEG ok ---')
    logging.info('--- Spleeter section ---')
    spleeter_mod = Spleeter(os.path.dirname(get_field("spleeter")),
                            stems)
    if spleeter_mod.install():
        logging.critical('SpleeterError: can\'t provide spleeter model')
        return 1
    spleeter_mod.execute(filename, analysis_folder)
    logging.info('--- Spleeter ok ---')
    logging.info('--- Bardsnote section ---')
    entrypoint(path, os.path.join(analysis_folder,
               os.path.splitext(os.path.basename(filename))[0], 'piano.wav'),
               os.path.splitext(os.path.basename(filename))[0])
    logging.info('--- Bardsnote ok ---')
    logging.info('--- PROGRAM OVER ---')
    return 0
