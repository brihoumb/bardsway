import os

import pickle
import numpy as np
from tqdm import tqdm

from .acoustic import wav2cqt
from .language import midi2roll

midi_dname = "MIDI"
audio_dname = "AUDIO"
dataset_dname = "MAPS_NEW"


def create_window(a, window_size):
    x, y = a.shape
    padded = np.pad(a.flatten(), int(window_size/2) * y, mode="constant")
    indexer = np.arange(window_size*y)[None, :] + y*np.arange(x)[:, None]
    b = padded[indexer]
    return np.reshape(b, (x, window_size, y, 1))


def preprocess_audio(audio_dir, window_size=7, output="to_pred.p",
                     sample_rate=16e3):
    X = np.empty((0, window_size, 264, 1))
    print(f"Creating dataset file \"{output}\". This may take a while")
    for f in tqdm(os.listdir(audio_dir), desc="Preprocessing files"):
        cqt = wav2cqt(os.path.join(audio_dir, f), sample_rate)
        window = create_window(cqt, window_size)
        print(f"cqt shape: {cqt.shape} \t window shape: {window.shape}")
        X = np.append(X, window, axis=0)
    print(X.shape)
    with open(output, 'wb') as handle:
        pickle.dump(X, handle, protocol=4)
