import os
import matplotlib.pyplot as plt
import numpy as np
import librosa
from librosa import display
import pandas as pd
import pickle
from tqdm import tqdm
from sklearn.preprocessing import scale


raw_dataset_path = "MAPS_NEW"
preprocessed_dataset_path = "PREPROCESSED"
audio_fname = "AUDIO"
pickle_fname = "acoustic_10.p"


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        print("already normalized")
        return v
    return v / norm


def plot_cqt(signal, sample_rate, name):
    fig = plt.figure(figsize=(12, 4))
    display.specshow(librosa.amplitude_to_db(np.abs(signal), ref=np.max),
                     sr=sample_rate, x_axis='time',
                     y_axis='cqt_note', hop_length=512, bins_per_octave=36,
                     fmin=librosa.note_to_hz('A0'))
    plt.colorbar(format='%+2.0f dB')
    plt.title(f'Constant-Q power spectrum - {name}')
    plt.tight_layout()
    plt.show()
    # plt.savefig(os.path.join("StandardGraphs", f"{name}_cqt.png"))
    plt.clf()
    fig.clf()


def wav2cqt(fname, sample_rate):
    signal, sr = librosa.load(fname)
    resampled = librosa.resample(signal, sr, sample_rate)
    cqt = librosa.cqt(resampled, sr=sample_rate, hop_length=512,
                      bins_per_octave=12*3, n_bins=264,
                      fmin=librosa.note_to_hz('A0'))
    # TODO: start fmin at 1/3 note lower than A0 because 3 bins per note

    cqt = np.abs(cqt)
    print("-- RAW --")
    print(f"min: {cqt.min()} max: {cqt.max()}")

    # --- STANDARDIZATION ---
    cqt = scale(cqt)
    print("-- STANDARDIZED --")
    print(f"min: {cqt.min()} max: {cqt.max()}")

    # -- NORMALIZATION --
    cqt = (cqt - cqt.min()) / (cqt.max() - cqt.min())
    print("-- NORMALIZED --")
    print(f"min: {cqt.min()} max: {cqt.max()}")

    # -- shape (264, n) -> (n, 264) --
    cqt = cqt.transpose()
    return cqt


def main():
    cqt = wav2cqt("MAPS_MUS-liz_et_trans5_ENSTDkCl.wav", 16e3)
    # print(cqt)
    # plot_cqt(cqt, 16e3, "MAPS_MUS-liz_et_trans5_ENSTDkCl")


if __name__ == '__main__':
    main()
