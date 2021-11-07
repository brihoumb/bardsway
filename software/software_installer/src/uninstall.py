import os
import shutil
import pathlib
from platform import system as which
from os.path import join, exists, basename


def add_to_path(path, level):
    destructured_path = list(pathlib.PurePath(path).parts)
    destructured_path.insert(len(destructured_path) - 1, level)
    return join(*destructured_path)


def uninstall(filepath):
    _isWindows = True if which() == 'Windows' else False
    libs = join(filepath, 'libs')
    ffmpeg = join(filepath, 'ffmpeg')
    models = join(filepath, 'models')
    config = join(filepath, 'config.json')
    symlink = join(filepath, f'bardsway{(".exe" if _isWindows else "")}')
    if (exists(filepath) and basename(filepath) == 'bardsway'):
        exists(config) and os.remove(config)
        exists(libs) and shutil.rmtree(libs)
        exists(ffmpeg) and shutil.rmtree(ffmpeg)
        exists(models) and shutil.rmtree(models)
        try:
            os.remove(symlink)
        except FileNotFoundError:
            pass
        return True
    elif (exists(join(filepath, 'bardsway'))):
        libs = add_to_path(libs, 'bardsway')
        ffmpeg = add_to_path(ffmpeg, 'bardsway')
        models = add_to_path(models, 'bardsway')
        config = add_to_path(config, 'bardsway')
        symlink = add_to_path(symlink, 'bardsway')
        exists(config) and os.remove(config)
        exists(libs) and shutil.rmtree(libs)
        exists(ffmpeg) and shutil.rmtree(ffmpeg)
        exists(models) and shutil.rmtree(models)
        try:
            os.remove(symlink)
        except FileNotFoundError:
            pass
        return True
    else:
        return False
