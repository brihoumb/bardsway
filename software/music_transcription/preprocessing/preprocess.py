import os

import numpy as np
import pickle
from tqdm import tqdm

from .acoustic import wav2cqt
from .language import midi2roll

dataset_dname = "MAPS_NEW"
audio_dname = "AUDIO"
midi_dname = "MIDI"


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


def preprocess_dataset(dataset_dir, window_size=7, output="data.p",
                       sample_rate=16e3):
    audio_dir = os.path.join(dataset_dir, audio_dname)
    midi_dir = os.path.join(dataset_dir, midi_dname)
    X, y = np.empty((0, window_size, 264, 1)), np.empty((0, 88))
    print(f"Creating dataset file \"{output}\". This may take a while")
    for f in tqdm(os.listdir(audio_dir), desc="Preprocessing files"):
        cqt = wav2cqt(os.path.join(audio_dir, f), sample_rate)
        roll = midi2roll(os.path.join(
            midi_dir, os.path.splitext(f)[0] + ".mid"), cqt.shape[0])
        window = create_window(cqt, window_size)
        print(f"cqt shape: {cqt.shape} \t window shape: {window.shape} \t" +
              "roll shape: {roll.shape}")
        X = np.append(X, window, axis=0)
        y = np.append(y, roll, axis=0)
    print(X.shape)
    print(y.shape)
    with open(output, 'wb') as handle:
        pickle.dump({"X": X, "y": y}, handle, protocol=4)


def main():
    preprocess_dataset(
        dataset_dname, output="/datadisk/music_transcription/data.p")


if __name__ == '__main__':
    main()
