import os

import pickle
import librosa
import numpy as np
import pandas as pd
from tqdm import tqdm
from librosa import display
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale


audio_fname = "AUDIO"
raw_dataset_path = "MAPS_NEW"
pickle_fname = "acoustic_10.p"
preprocessed_dataset_path = "PREPROCESSED"


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
